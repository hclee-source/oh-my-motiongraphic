// 영상 화면 배치 검사: 영상을 일정 간격(기본 0.2초)으로 넘기며 화면에 보이는 글자와 카드의 위치를 재서
// 글자끼리 겹침, 글자와 자막 겹침, 글자가 카드·화면 밖으로 넘침, 카드끼리 겹침, 잘린 글자를 찾는다.
// 화면에 나온 글자 목록(장면별, 보인 시각, 글자 크기)도 함께 적는다.
//
// 사용(저장소 맨 위에서): node tools/check_layout.mjs <편 폴더 또는 영상 폴더> [--step 0.2] [--from 0] [--to 끝]
//   개념 영상: concept/episodes/<편> (쇼츠: .../<편>/shorts), 이벤트 쇼츠: videos/notice-<이름>
// 결과: <편 폴더>/video/boards/review/layout-report.json + 화면 요약
//
// HyperFrames 0.8.214 안의 페이지 열기·시각 이동 기능을 빌려 쓴다(버전이 바뀌면 찾는 이름을 확인할 것).
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const HF_VERSION = "0.8.214";

function arg(name, def) {
  const i = process.argv.indexOf(`--${name}`);
  return i > 0 ? process.argv[i + 1] : def;
}
const episode = path.resolve(process.argv[2] ?? ".");
// 편 폴더(안에 video/)도, HyperFrames 프로젝트 폴더(안에 index.html)도 받는다
const projectDir = fs.existsSync(path.join(episode, "index.html")) ? episode : path.join(episode, "video");
const STEP = Number(arg("step", "0.2"));
const FROM = Number(arg("from", "0"));
const TO = arg("to", null);

function findHyperframesDist() {
  const base = path.join(os.homedir(), "AppData", "Local", "npm-cache", "_npx");
  for (const d of fs.readdirSync(base)) {
    const pkg = path.join(base, d, "node_modules", "hyperframes", "package.json");
    if (fs.existsSync(pkg) && JSON.parse(fs.readFileSync(pkg, "utf8")).version === HF_VERSION) {
      return path.dirname(pkg);
    }
  }
  throw new Error(`hyperframes@${HF_VERSION} 설치본을 못 찾음 — 영상 폴더에서 'npm run check'를 한 번 돌려 받아 둘 것`);
}

const hfDir = findHyperframesDist();
const dist = path.join(hfDir, "dist");
const distFiles = fs.readdirSync(dist).filter((f) => f.endsWith(".js"));
async function importExporting(name) {
  const re = new RegExp(`export \\{[^}]*\\b${name}\\b`, "s");
  for (const f of distFiles) {
    const text = fs.readFileSync(path.join(dist, f), "utf8");
    if (text.includes(`function ${name}`) && re.test(text)) return import(pathToFileURL(path.join(dist, f)).href);
  }
  throw new Error(`HyperFrames 안에서 ${name}을 못 찾음`);
}

const { bundleToSingleHtml } = await importExporting("bundleToSingleHtml");
const { serveStaticProjectHtml } = await importExporting("serveStaticProjectHtml");
const seekMod = await importExporting("seekCompositionTimeline");
const { ensureBrowser } = await importExporting("ensureBrowser");
const puppeteer = (await import(pathToFileURL(path.join(hfDir, "..", "puppeteer-core", "lib", "puppeteer", "puppeteer-core.js")).href)).default;

// ───────── 페이지 안에서 도는 측정 ─────────
function pageAudit() {
  const root = document.querySelector("[data-composition-id=main]");
  const W = Number(root?.getAttribute("data-width")) || 1920, H = Number(root?.getAttribute("data-height")) || 1080;
  // 쇼츠(세로)는 위 메뉴, 아래 채널 이름·설명, 오른쪽 좋아요 버튼이 덮는 자리를 피한다
  const SHORTS = H > W;
  const covered = (r) => r.t < 140 || r.b > 1450 || (r.r > 960 && r.b > 1000);
  const CARD_CLASSES = ["x-card", "x-dark", "x-side"];
  const isCard = (el) => CARD_CLASSES.some((c) => el.classList.contains(c));

  const opCache = new Map();
  const effOpacity = (el) => {
    if (!el || el.nodeType !== 1) return 1;
    if (opCache.has(el)) return opCache.get(el);
    const cs = getComputedStyle(el);
    let v = cs.visibility === "visible" ? Number(cs.opacity) : 0;
    if (v > 0) v *= effOpacity(el.parentElement);
    opCache.set(el, v);
    return v;
  };
  const sceneOf = (el) => el.closest("[data-composition-id]")?.getAttribute("data-composition-id") ?? "?";
  const keyOf = (el) => {
    const parts = [];
    let e = el;
    while (e && e.nodeType === 1 && !e.hasAttribute("data-composition-id")) {
      if (e.id) { parts.unshift("#" + e.id); break; }
      const cls = [...e.classList].filter((c) => c !== "x-hide").slice(0, 2).join(".");
      const idx = e.parentElement ? [...e.parentElement.children].indexOf(e) + 1 : 1;
      parts.unshift(`${e.tagName.toLowerCase()}${cls ? "." + cls : ""}:${idx}`);
      e = e.parentElement;
    }
    return `${sceneOf(el)} ${parts.join(">")}`;
  };
  const union = (rects) => {
    let l = Infinity, t = Infinity, r = -Infinity, b = -Infinity;
    for (const q of rects) {
      if (q.width < 0.5 || q.height < 0.5) continue;
      l = Math.min(l, q.left); t = Math.min(t, q.top); r = Math.max(r, q.right); b = Math.max(b, q.bottom);
    }
    return l === Infinity ? null : { l, t, r, b };
  };
  const inter = (a, b) => {
    const w = Math.min(a.r, b.r) - Math.max(a.l, b.l), h = Math.min(a.b, b.b) - Math.max(a.t, b.t);
    return w > 0 && h > 0 ? { w, h } : null;
  };
  // 넘침을 잘라 내는 조상(overflow hidden) 안쪽으로 자른다
  const clipToAncestors = (el, rect) => {
    let r = { ...rect };
    for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflowX !== "visible" || cs.overflowY !== "visible") {
        const q = e.getBoundingClientRect();
        r = { l: Math.max(r.l, q.left), t: Math.max(r.t, q.top), r: Math.min(r.r, q.right), b: Math.min(r.b, q.bottom) };
        if (r.r <= r.l || r.b <= r.t) return null;
      }
    }
    return r;
  };

  // 글자 칸(줄 높이)이 아니라 실제 획이 닿는 위아래 범위로 줄인다 — 큰 숫자는 칸 위아래가 많이 빈다
  const ctx = document.createElement("canvas").getContext("2d");
  const inkRects = (rects, text, cs) => {
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    ctx.letterSpacing = cs.letterSpacing === "normal" ? "0px" : cs.letterSpacing;
    const m = ctx.measureText(text);
    const fh = m.fontBoundingBoxAscent + m.fontBoundingBoxDescent;
    return rects.map((q) => {
      const k = q.height / fh;
      return { left: q.left, right: q.right, width: q.width, height: q.height,
        top: q.top + (m.fontBoundingBoxAscent - m.actualBoundingBoxAscent) * k,
        bottom: q.top + (m.fontBoundingBoxAscent + m.actualBoundingBoxDescent) * k };
    });
  };

  // 1) 글자 묶음: 직접 글자를 가진 요소마다 하나
  const texts = [];
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (!n.nodeValue.trim()) continue;
    const el = n.parentElement;
    if (!el || seen.has(el) || el.closest("script,style,template,audio,video")) continue;
    seen.add(el);
    const op = effOpacity(el);
    if (op < 0.05) continue;
    const rects = [];
    for (const c of el.childNodes) {
      if (c.nodeType !== 3 || !c.nodeValue.trim()) continue;
      const range = document.createRange();
      range.selectNodeContents(c);
      rects.push(...range.getClientRects());
    }
    const cs = getComputedStyle(el);
    const text = [...el.childNodes].filter((c) => c.nodeType === 3).map((c) => c.nodeValue).join("").trim();
    const u = union(inkRects(rects, text, cs));
    if (!u) continue;
    const rect = clipToAncestors(el, u);
    if (!rect) continue;
    const lines = new Set(rects.filter((q) => q.width > 1).map((q) => Math.round(q.top / 4))).size;
    texts.push({
      el, key: keyOf(el), scene: sceneOf(el), op: +op.toFixed(2), rect, raw: u, lines, text,
      size: parseFloat(cs.fontSize), card: el.closest(CARD_CLASSES.map((c) => "." + c).join(",")),
      cap: sceneOf(el) === "captions",
    });
  }

  // 2) 카드
  const cards = [];
  for (const el of document.querySelectorAll(CARD_CLASSES.map((c) => "." + c).join(","))) {
    const op = effOpacity(el);
    if (op < 0.05) continue;
    const q = el.getBoundingClientRect();
    if (q.width < 2 || q.height < 2) continue;
    cards.push({ el, key: keyOf(el), op: +op.toFixed(2), rect: { l: q.left, t: q.top, r: q.right, b: q.bottom } });
  }

  // 3) 도형: 글자 없는 상자 가운데 색이 칠해졌거나 테두리가 보이는 것(막대, 점, 선, 강조 테두리)
  const visibleColor = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return false; const p = m[1].split(",").map(Number); return p.length < 4 || p[3] > 0.05; };
  const shapes = [];
  for (const el of document.querySelectorAll("[data-composition-id] *")) {
    if (isCard(el) || el.closest("script,style,template")) continue;
    if (el.textContent.trim()) continue;
    const cs = getComputedStyle(el);
    const fill = visibleColor(cs.backgroundColor) || cs.backgroundImage !== "none";
    const line = ["Top", "Right", "Bottom", "Left"].some((s) => parseFloat(cs[`border${s}Width`]) > 0 && visibleColor(cs[`border${s}Color`]));
    if (!fill && !line) continue;
    const q = el.getBoundingClientRect();
    if (q.width * q.height < 60 || q.width * q.height > W * H * 0.5) continue;
    const op = effOpacity(el);
    if (op < 0.15) continue;
    shapes.push({ el, key: keyOf(el), op: +op.toFixed(2), rect: { l: q.left, t: q.top, r: q.right, b: q.bottom } });
  }

  const issues = [];
  const R = (r) => [Math.round(r.l), Math.round(r.t), Math.round(r.r), Math.round(r.b)];
  const brief = (x) => ({ key: x.key, text: x.text, op: x.op, rect: R(x.rect) });
  const gap = (a, b) => Math.max(Math.max(a.l, b.l) - Math.min(a.r, b.r), Math.max(a.t, b.t) - Math.min(a.b, b.b));
  // 한 줄 안에서 이어지는 조각(글자를 쪼개 둔 span 등)은 붙어 있어도 정상
  const blockOf = (el) => { let e = el.classList.contains("x-ov") ? el.parentElement : el; while (e.parentElement && getComputedStyle(e).display.startsWith("inline")) e = e.parentElement; return e; };
  const sameLine = (a, b) => blockOf(a.el) === blockOf(b.el) &&
    Math.min(a.rect.b, b.rect.b) - Math.max(a.rect.t, b.rect.t) > 0.5 * Math.min(a.rect.b - a.rect.t, b.rect.b - b.rect.t);
  // 불투명한 장면(data-layout-cover)이 다른 장면을 덮으며 들어올 때(밀어 올리기, 원 퍼짐) 두 장면의 글자는 같이 보이지 않는다
  const coverOf = (el) => el.closest("[data-layout-cover]");
  const coverSplit = (a, b) => { const ca = coverOf(a), cb = coverOf(b); return !!(ca || cb) && ca !== cb; };

  // 글자끼리 / 글자와 자막 / 너무 붙은 글자
  for (let i = 0; i < texts.length; i++) {
    for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      if (Math.min(a.op, b.op) < 0.15) continue;
      // 같은 글자를 같은 자리에 겹쳐 둔 색 바꿈용 덧칠(x-ov)은 하나로 본다
      if (a.text === b.text && Math.abs(a.rect.l - b.rect.l) < 3 && Math.abs(a.rect.t - b.rect.t) < 3) continue;
      // 글자가 바뀌는 자리(data-layout-allow-overlap)에서 옛 글자와 새 글자가 엇갈리는 것은 의도한 것
      const allowA = a.el.closest("[data-layout-allow-overlap]");
      if (allowA && allowA === b.el.closest("[data-layout-allow-overlap]")) continue;
      if (coverSplit(a.el, b.el)) continue;
      const x = inter(a.rect, b.rect);
      if (x && x.w >= 3 && x.h >= 3) {
        issues.push({ kind: a.cap || b.cap ? "caption" : "text", a: brief(a), b: brief(b), minOp: Math.min(a.op, b.op), area: Math.round(x.w * x.h) });
      } else if (!a.cap && !b.cap && !sameLine(a, b)) {
        const g = gap(a.rect, b.rect);
        const limit = Math.max(10, Math.min(a.size, b.size) * 0.25);
        if (g < limit) issues.push({ kind: "near", a: brief(a), b: brief(b), minOp: Math.min(a.op, b.op), over: Math.round(g) });
      }
    }
  }
  // 글자와 도형: 도형이 글자를 통째로 감싸면(바탕·강조 칸) 괜찮고, 걸치거나 글자 안에 박히면 문제
  for (const t of texts) {
    if (t.op < 0.15) continue;
    for (const s of shapes) {
      if (s.el.contains(t.el) || Math.min(s.op, t.op) < 0.15) continue;
      if (coverSplit(s.el, t.el)) continue;
      // 일부러 글자 위에 긋는 도형(취소선 등): 글자와 도형을 함께 감싼 요소에 data-layout-allow-overlap을 붙인다
      const allowS = s.el.closest("[data-layout-allow-overlap]");
      if (allowS && allowS.contains(t.el)) continue;
      const x = inter(t.rect, s.rect);
      if (!x || x.w < 3 || x.h < 3) continue;
      const wraps = s.rect.l <= t.rect.l + 2 && s.rect.t <= t.rect.t + 2 && s.rect.r >= t.rect.r - 2 && s.rect.b >= t.rect.b - 2;
      if (!wraps) issues.push({ kind: "shape", a: brief(t), b: { key: s.key, op: s.op, rect: R(s.rect) }, minOp: Math.min(s.op, t.op) });
    }
  }
  for (const t of texts) {
    if (t.op < 0.15) continue;
    const r = t.rect;
    // 화면 밖
    if (r.l < -2 || r.t < -2 || r.r > W + 2 || r.b > H + 2) issues.push({ kind: "frame", a: brief(t), minOp: t.op });
    else if (SHORTS && covered(r)) issues.push({ kind: "safe", a: brief(t), minOp: t.op });
    // 카드 밖 / 카드 가장자리에 바짝 붙음(안쪽 여백 16px 미만)
    if (t.card) {
      const q = t.card.getBoundingClientRect();
      const over = Math.max(q.left - r.l, q.top - r.t, r.r - q.right, r.b - q.bottom);
      if (over > 2) issues.push({ kind: "card", a: brief(t), b: { key: keyOf(t.card) }, minOp: t.op, over: Math.round(over) });
      else if (over > -16) issues.push({ kind: "edge", a: brief(t), b: { key: keyOf(t.card) }, minOp: t.op, over: Math.round(-over) });
    }
    // 내 카드가 아닌 카드 위에 얹히거나 바짝 붙은 글자
    if (!t.cap) {
      for (const c of cards) {
        if (c.el.contains(t.el) || Math.min(c.op, t.op) < 0.15) continue;
        if (t.card && (t.card.contains(c.el) || c.el.contains(t.card))) continue;
        const x = inter(t.rect, c.rect);
        if (x && x.w > 4 && x.h > 6) issues.push({ kind: "textOnCard", a: brief(t), b: { key: c.key, op: c.op, rect: R(c.rect) }, minOp: Math.min(c.op, t.op) });
        else if (!x && gap(t.rect, c.rect) < 16) issues.push({ kind: "nearCard", a: brief(t), b: { key: c.key, op: c.op, rect: R(c.rect) }, minOp: Math.min(c.op, t.op), over: Math.round(gap(t.rect, c.rect)) });
      }
    }
  }
  // 카드끼리
  for (let i = 0; i < cards.length; i++) {
    for (let j = i + 1; j < cards.length; j++) {
      const a = cards[i], b = cards[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      if (Math.min(a.op, b.op) < 0.15) continue;
      const x = inter(a.rect, b.rect);
      if (x && x.w > 4 && x.h > 4) issues.push({ kind: "cards", a: { key: a.key, op: a.op, rect: R(a.rect) }, b: { key: b.key, op: b.op, rect: R(b.rect) }, minOp: Math.min(a.op, b.op) });
    }
  }
  // 잘린 글자: 그 글자 자체가 넘침 숨김 상자 밖으로 삐져나가 잘린 경우만(다른 요소가 넘쳐서 생긴 스크롤은 무시)
  for (const t of texts) {
    if (t.op < 0.15) continue;
    for (let e = t.el.parentElement; e && e !== document.body; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.overflowX === "visible" && cs.overflowY === "visible") continue;
      const q = e.getBoundingClientRect();
      const out = Math.max(q.left - t.raw.l, q.top - t.raw.t, t.raw.r - q.right, t.raw.b - q.bottom);
      if (out > 2) {
        issues.push({ kind: "clipped", a: brief(t), b: { key: keyOf(e) }, minOp: t.op, over: Math.round(out) });
        break;
      }
    }
  }

  return {
    issues,
    texts: texts.map((t) => ({ key: t.key, scene: t.scene, text: t.text, op: t.op, size: t.size, lines: t.lines, rect: R(t.rect), cap: t.cap })),
  };
}

// ───────── 실행 ─────────
const html = await bundleToSingleHtml(projectDir);
const sizeMatch = fs.readFileSync(path.join(projectDir, "index.html"), "utf8").match(/data-composition-id="main"[^>]*data-width="(\d+)" data-height="(\d+)"/);
const [VW, VH] = sizeMatch ? [Number(sizeMatch[1]), Number(sizeMatch[2])] : [1920, 1080];
const server = await serveStaticProjectHtml(projectDir, html, "검사용 서버를 못 열었음");
const chrome = await ensureBrowser();
const browser = await puppeteer.launch({
  headless: true,
  executablePath: chrome.executablePath,
  args: [`--window-size=${VW},${VH}`, "--hide-scrollbars", "--mute-audio", "--autoplay-policy=no-user-gesture-required"],
});
let report;
try {
  const page = await browser.newPage();
  await seekMod.installPageFunctionGuard(page);
  await page.setViewport({ width: VW, height: VH });
  await page.goto(server.url, { waitUntil: "load", timeout: 60000 });
  await seekMod.waitForRuntimeReady(page, 15000);
  await seekMod.waitForCompositionFonts(page, 3000);
  const duration = await page.evaluate(() => {
    const root = document.querySelector("[data-composition-id]");
    const d = Number(root?.getAttribute("data-duration"));
    if (d > 0) return d;
    const tl = Object.values(window.__timelines ?? {})[0];
    return tl?.duration?.() ?? 0;
  });
  const end = TO !== null ? Math.min(Number(TO), duration) : duration;
  await page.addScriptTag({ content: `window.__certAudit = ${pageAudit.toString()};` });

  const samples = [];
  for (let t = FROM; t < end - 0.01; t = +(t + STEP).toFixed(3)) samples.push(t);
  const found = new Map();   // 겹침 종류+대상 → 보인 시각들
  const inventory = new Map(); // 글자 → 보인 시각들
  const started = Date.now();
  for (const [i, t] of samples.entries()) {
    await seekMod.seekCompositionTimeline(page, t, seekMod.AUDIT_SEEK_OPTIONS);
    const res = await page.evaluate(() => window.__certAudit());
    for (const is of res.issues) {
      const k = `${is.kind}|${is.a.key}|${is.b?.key ?? ""}`;
      if (!found.has(k)) found.set(k, { kind: is.kind, a: is.a, b: is.b, hits: [] });
      const f = found.get(k);
      f.hits.push({ t, minOp: is.minOp, area: is.area, over: is.over, aText: is.a.text, bText: is.b?.text });
    }
    for (const tx of res.texts) {
      if (tx.cap) continue;
      if (!inventory.has(tx.key)) inventory.set(tx.key, { key: tx.key, scene: tx.scene, size: tx.size, texts: new Set(), hits: [], maxLines: 1 });
      const it = inventory.get(tx.key);
      it.texts.add(tx.text);
      it.maxLines = Math.max(it.maxLines, tx.lines);
      if (tx.op >= 0.5) it.hits.push(t);
    }
    if (i % 200 === 0) process.stderr.write(`  ${t.toFixed(1)}초 / ${end.toFixed(1)}초\n`);
  }

  const spans = (times) => {
    const out = [];
    for (const t of times) {
      const last = out[out.length - 1];
      if (last && t - last[1] <= STEP * 1.6) last[1] = t;
      else out.push([t, t]);
    }
    return out.map(([a, b]) => ({ from: a, to: +(b + STEP).toFixed(2), len: +(b - a + STEP).toFixed(2) }));
  };
  const issues = [];
  for (const f of found.values()) {
    for (const s of spans(f.hits.map((h) => h.t))) {
      const hs = f.hits.filter((h) => h.t >= s.from - 1e-6 && h.t < s.to - 1e-6);
      const maxOp = Math.max(...hs.map((h) => h.minOp));
      // 확실: 둘 다 또렷한 채로 0.4초 넘게 겹침 / 잠깐: 바뀌는 순간에만 스침
      const level = maxOp >= 0.6 && s.len >= 0.4 ? "확실" : "잠깐";
      const GAP_KINDS = ["near", "nearCard", "edge"];
      const over = GAP_KINDS.includes(f.kind) ? Math.min(...hs.map((h) => h.over)) : Math.max(0, ...hs.map((h) => h.over ?? 0)) || undefined;
      issues.push({ level, kind: f.kind, from: s.from, to: s.to, len: s.len, maxOp, a: f.a.key, aText: hs[0].aText, b: f.b?.key, bText: hs[0].bText, over });
    }
  }
  issues.sort((x, y) => (x.level === y.level ? x.from - y.from : x.level === "확실" ? -1 : 1));
  const texts = [...inventory.values()]
    .map((it) => ({ scene: it.scene, key: it.key, size: it.size, maxLines: it.maxLines, texts: [...it.texts], shown: spans(it.hits) }))
    .sort((a, b) => (a.shown[0]?.from ?? 1e9) - (b.shown[0]?.from ?? 1e9));
  report = { step: STEP, duration, samples: samples.length, seconds: Math.round((Date.now() - started) / 1000), issues, texts };
} finally {
  await browser.close().catch(() => {});
  await server.close();
}

const outDir = path.join(projectDir, "boards", "review");
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "layout-report.json"), JSON.stringify(report, null, 1), "utf8");

const KIND = { text: "글자끼리 겹침", caption: "자막과 겹침", frame: "화면 밖", card: "카드 밖으로 넘침", textOnCard: "다른 카드 위 글자", cards: "카드끼리 겹침", clipped: "잘린 글자", shape: "글자와 도형 겹침", near: "글자끼리 너무 붙음", nearCard: "다른 카드에 바짝 붙은 글자", edge: "카드 가장자리에 바짝 붙은 글자", safe: "쇼츠 화면 가림 자리" };
const sure = report.issues.filter((x) => x.level === "확실");
const brief = report.issues.filter((x) => x.level !== "확실");
console.log(`검사 ${report.samples}장면(${STEP}초 간격, ${report.seconds}초 걸림) — 확실 ${sure.length}건, 잠깐 스침 ${brief.length}건`);
for (const x of sure) {
  console.log(`[${KIND[x.kind]}] ${x.from.toFixed(1)}~${x.to.toFixed(1)}초 (${x.len}초) ${x.a} ‘${x.aText ?? ""}’${x.b ? `  ↔  ${x.b}${x.bText ? ` ‘${x.bText}’` : ""}` : ""}${["near", "nearCard", "edge"].includes(x.kind) ? `  간격 ${x.over}px` : x.over ? `  넘침 ${x.over}px` : ""}`);
}
const small = report.texts.filter((t) => t.size < 34 && t.shown.length);
console.log(`작은 글씨(34px 미만) ${small.length}개, 1초 미만으로만 보인 글자 ${report.texts.filter((t) => t.shown.length && Math.max(...t.shown.map((s) => s.len)) < 1).length}개, 두 줄 넘게 꺾인 글자 ${report.texts.filter((t) => t.maxLines > 1).length}개`);
