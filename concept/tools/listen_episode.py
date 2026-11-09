"""문장 소리 파일(sNN.wav)을 받아 적어(음성 인식 large-v3-turbo) 읽을 말과 대조하고, 낱말 시각을 남긴다.

사용(저장소 맨 위에서): python concept/tools/listen_episode.py concept/episodes/<편> [concept/episodes/<편>/shorts ...] [--only 3,5]
결과(프로젝트 폴더 안):
  listen/words.json  — {"문장 번호": {"say": 읽은 말, "words": [[시작, 끝, 낱말], ...]}} (시각은 그 문장 시작 기준 초)
  listen/report.txt  — 문장마다 일치도와 받아 적은 말(▲ = 0.9 미만, 직접 확인할 것)
--only가 없으면, 읽을 말이 바뀐 문장만 다시 듣는다(say가 같으면 앞 결과를 쓴다).
준비: uv pip install --python .venv/Scripts/python.exe faster-whisper (처음 한 번 모델을 내려받는다, 약 1.6GB)
대조는 verify_episode.py --words가 이 파일을 읽어 한다(그림 시각·자막 나눔 대조, word_times.json 쓰기).
"""
import difflib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_episode import norm  # noqa: E402

MODEL = "large-v3-turbo"


def main():
    import soundfile as sf, librosa
    from faster_whisper import WhisperModel
    args = sys.argv[1:]
    only = None
    if "--only" in args:
        i = args.index("--only")
        only = set(args[i + 1].split(","))
        args = args[:i] + args[i + 2:]
    model = None
    for proj in map(Path, args):
        tl = json.loads((proj / "timeline.json").read_text(encoding="utf-8"))
        ss = [s for c in tl["chapters"] for s in c["sentences"]]
        out = proj / "listen"
        out.mkdir(exist_ok=True)
        wf = out / "words.json"
        old = json.loads(wf.read_text(encoding="utf-8")) if wf.exists() else {}
        res, lines, t0, heard = {}, [], time.time(), 0
        for s in ss:
            key = str(s["n"])
            want = re.sub(r"\s*\|\s*", " ", s["say"])
            if key in old and old[key]["say"] == want and (only is None or key not in only):
                res[key] = old[key]
            else:
                if model is None:
                    model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=14)
                x, sr = sf.read(proj / f"video/assets/vo/s{s['n']:02d}.wav", dtype="float32")
                x = librosa.resample(x, orig_sr=sr, target_sr=16000)
                # beam_size=1(가장 그럴듯한 낱말만 바로 고르기): 2026-11-05 여러 편을 함께 만들 때 5로는 한 편에 20분 가까이 걸려 줄임.
                # 빠진 음절·숫자를 찾는 용도라 정확도 차이는 작다(▲가 조금 더 뜰 수 있으니 하나씩 확인)
                segs, _ = model.transcribe(x, language="ko", beam_size=1, vad_filter=False, word_timestamps=True,
                                           condition_on_previous_text=False)
                res[key] = {"say": want, "words": [[round(w.start, 3), round(w.end, 3), w.word] for g in segs for w in g.words]}
                heard += 1
            got = "".join(w[2] for w in res[key]["words"]).strip()
            r = difflib.SequenceMatcher(None, norm(want), norm(got)).ratio()
            lines.append(f"{'▲' if r < 0.9 else ' '} {s['n']:>2}번 {r:.2f} | 읽을 말: {want} | 받아 적음: {got}")
        wf.write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
        (out / "report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        bad = sum(l.startswith("▲") for l in lines)
        print(f"{proj}: 문장 {len(ss)}개(새로 들은 것 {heard}), 일치 0.9 미만 {bad}개, {time.time() - t0:.0f}초", flush=True)


if __name__ == "__main__":
    main()
