"""한 편의 내레이션을 만든다: script.md 문장마다 AI 음성 → 앞뒤 공백 자르기 → 이어 붙인 narration.wav + timeline.json

사용(저장소 맨 위에서): python concept/tools/tts_episode.py concept/episodes/<편> [--voice ko-KR-InJoonNeural] [--rate +0%] [--pitch +0Hz]
쇼츠: python concept/tools/tts_episode.py concept/episodes/<편>/shorts --title-dur 0 --sent-gap 0.2 --chapter-gap 0.45 --tail 1.0
"""
import argparse, asyncio, hashlib, json, re, subprocess, sys, wave
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")

TITLE_DUR = 3.6      # 여는 제목 장면 길이(초)
SENT_GAP = 0.35      # 문장 사이 쉼
CHAPTER_GAP = 0.9    # 장 사이 쉼
TAIL = 1.6           # 마지막 문장 뒤 여운
RATE = 48000

def parse_script(path):
    chapters, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            cur = {"n": int(m.group(1)), "title": m.group(2).strip(), "sentences": []}
            chapters.append(cur)
            continue
        m = re.match(r"^(\d+)\. (.+)$", line)
        if m and cur is not None:
            cur["sentences"].append({"n": int(m.group(1)), "text": m.group(2).strip()})
    return chapters

def to_wav_trimmed(src, dst):
    af = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.03,areverse,"
          "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-af", af,
                    "-ar", str(RATE), "-ac", "1", "-sample_fmt", "s16", str(dst)], check=True)

def wav_frames(path):
    with wave.open(str(path), "rb") as w:
        return w.readframes(w.getnframes()), w.getnframes()

async def synth(text, voice, rate, pitch, out):
    await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(out))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--voice", default="ko-KR-InJoonNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--pitch", default="+0Hz")
    ap.add_argument("--title-dur", type=float, default=TITLE_DUR)
    ap.add_argument("--sent-gap", type=float, default=SENT_GAP)
    ap.add_argument("--chapter-gap", type=float, default=CHAPTER_GAP)
    ap.add_argument("--tail", type=float, default=TAIL)
    a = ap.parse_args()

    ep = Path(a.episode)
    vo = ep / "video" / "assets" / "vo"
    (vo / "raw").mkdir(parents=True, exist_ok=True)
    say = {k: v for k, v in json.loads((ep / "say.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
    chapters = parse_script(ep / "script.md")

    pcm, t = bytearray(), 0.0
    def pad(sec):
        nonlocal t
        pcm.extend(b"\x00\x00" * int(round(sec * RATE)))
        t += sec

    pad(a.title_dur)
    for ci, ch in enumerate(chapters):
        if ci:
            pad(a.chapter_gap)
        ch["start"] = round(t, 3)
        for si, s in enumerate(ch["sentences"]):
            if si:
                pad(a.sent_gap)
            # ‘|’는 자막을 끊을 자리 표시(쇼츠). 소리에는 쓰지 않는다.
            s["say"] = re.sub(r"\s*\|\s*", " ", say.get(str(s["n"]), s["text"])).replace("‘", "").replace("’", "")
            key = hashlib.sha1(f'{a.voice}|{a.rate}|{a.pitch}|{s["say"]}'.encode()).hexdigest()[:10]
            raw = vo / "raw" / f's{s["n"]:02d}-{key}.mp3'
            if not raw.exists():
                asyncio.run(synth(s["say"], a.voice, a.rate, a.pitch, raw))
            wav = vo / f's{s["n"]:02d}.wav'
            to_wav_trimmed(raw, wav)
            frames, n = wav_frames(wav)
            s["start"] = round(t, 3)
            s["dur"] = round(n / RATE, 3)
            pcm.extend(frames)
            t += n / RATE
        ch["end"] = round(t, 3)
        print(f'{ch["n"]:>2}장 {ch["title"]:<12} {ch["start"]:7.2f} ~ {ch["end"]:7.2f}초')
    pad(a.tail)

    with wave.open(str(vo / "narration.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(bytes(pcm))
    timeline = {"voice": a.voice, "rate": a.rate, "pitch": a.pitch, "title_dur": a.title_dur,
                "total": round(t, 3), "chapters": chapters}
    (ep / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"전체 {t:.1f}초 ({t / 60:.1f}분)")

if __name__ == "__main__":
    main()
