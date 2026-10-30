"""윈도우 알림(화면 오른쪽 아래) 띄우기. 누르면 지정한 폴더가 열린다.

사용(다른 스크립트에서): from notify import notify; notify("제목", "내용", r"C:\\...\\renders")
시험: python notices/notify.py
메일 대신 쓰는 이유: 회사 구글 계정은 앱 비밀번호가 막혀 있고(보안 정책), 아웃룩은 자동 발송 때 확인 창이 뜬다.
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

# 윈도우 PowerShell의 앱 이름으로 알림을 띄운다(따로 등록할 필요 없음)
APP_ID = r"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"

def notify(title, body, folder=None):
    launch = ""
    actions = ""
    if folder:
        uri = Path(folder).resolve().as_uri()
        launch = f' activationType="protocol" launch="{html.escape(uri)}"'
        actions = f'<actions><action content="폴더 열기" activationType="protocol" arguments="{html.escape(uri)}"/></actions>'
    xml = (f'<toast{launch}><visual><binding template="ToastGeneric">'
           f'<text>{html.escape(title)}</text><text>{html.escape(body)}</text>'
           f'</binding></visual>{actions}</toast>')
    ps = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml(@'
{xml}
'@)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('{APP_ID}').Show($toast)
"""
    # 한글이 깨지지 않게 BOM 붙은 UTF-8 파일로 넘긴다(윈도우 PowerShell 5.1)
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8-sig") as f:
        f.write(ps)
        script = f.name
    try:
        # 창 없이 실행(작업 스케줄러에서 pythonw로 돌 때 검은 창이 번쩍이지 않게)
        r = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script],
                           capture_output=True, text=True, timeout=60,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    finally:
        Path(script).unlink(missing_ok=True)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    here = Path(__file__).resolve().parent.parent / "videos" / "notice-adsp-51-lecture" / "renders"
    notify("합격빠따 알림 (시험)", "공지 쇼츠가 준비되면 이렇게 알려 드립니다. 누르면 결과 폴더가 열립니다.", here)
    print("알림을 보냈습니다")
