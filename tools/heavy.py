"""무거운 명령(배치 검사·사진 찍기·받아 적기·렌더)을 한 번에 하나만 돌게 줄 세운다.

이 PC는 남는 메모리가 2GB 남짓이라, 여러 작업이 동시에 브라우저나 음성 인식 모델을 띄우면 강제 종료된다.
여러 편을 함께 만들 때 무거운 명령 앞에 붙인다(저장소 맨 위에서):
  .venv/Scripts/python.exe tools/heavy.py bash concept/tools/check_episode.sh concept/episodes/<편>
  .venv/Scripts/python.exe tools/heavy.py --wait 300 node tools/check_layout.mjs concept/episodes/<편>
- 차례가 오면 명령을 그대로 실행하고 그 종료 코드를 돌려준다.
- --wait 초(기본 540) 안에 차례가 안 오면 실행하지 않고 종료 코드 75로 끝난다 → 잠시 뒤 같은 명령을 다시.
- 줄 세우는 열쇠는 운영체제 파일 잠금이라, 명령이 죽거나 창이 닫혀도 잠금이 저절로 풀린다.
"""
import os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
LOCK = Path(__file__).resolve().parent / ".heavy.lock"


def try_lock(f):
    if os.name == "nt":
        import msvcrt
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            return True
        except OSError:
            return False
    import fcntl
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def main():
    args = sys.argv[1:]
    wait = 540
    if args[:1] == ["--wait"]:
        wait, args = int(args[1]), args[2:]
    if not args:
        sys.exit(__doc__)
    LOCK.touch(exist_ok=True)
    f = open(LOCK, "r+b")
    t0 = time.time()
    told = False
    while not try_lock(f):
        if time.time() - t0 > wait:
            print(f"[heavy] 다른 무거운 작업이 {wait}초 넘게 돌고 있어 실행하지 않았습니다. 잠시 뒤 같은 명령을 다시 실행하세요.", flush=True)
            sys.exit(75)
        if not told:
            print("[heavy] 다른 무거운 작업이 끝나기를 기다리는 중…", flush=True)
            told = True
        time.sleep(3)
    waited = time.time() - t0
    if waited > 3:
        print(f"[heavy] {waited:.0f}초 기다린 뒤 실행", flush=True)
    cmd = list(args)
    if os.name == "nt":
        # 윈도우는 ‘.venv/Scripts/python.exe’처럼 상대 경로·빗금으로 적은 실행 파일을 못 찾는다 → 절대 경로로
        exe = Path(cmd[0])
        if exe.exists():
            cmd[0] = str(exe.resolve())
        else:
            import shutil
            found = shutil.which(cmd[0]) or shutil.which(cmd[0] + ".cmd")
            if found:
                cmd[0] = found
    sys.exit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()
