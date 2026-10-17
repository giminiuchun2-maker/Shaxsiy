"""Yangi versiyani GitHub'ga FAQAT hovuz bo'sh bo'lganda joylaydi (ishlayotgan va navbatdagi boblar tugagach).
   python deploy-when-idle.py <GITHUB_TOKEN>      (hisob giminiuchun2-maker; setup.py ni o'zi chaqiradi)"""
import json, subprocess, sys, time, urllib.request
from pathlib import Path

H = Path(__file__).parent
gate = json.loads((Path.home() / "manhwa-gate" / ".secrets.atomic.json").read_text(encoding="utf-8"))
URL = "https://manhwa-gate-atomic.compass-crm.workers.dev/jobs/list?w=deploy-check"


def busy() -> int:
    r = urllib.request.Request(URL, headers={"x-key": gate["GATE_KEY"], "user-agent": "manhwa-bot/1.0"})
    rows = json.loads(urllib.request.urlopen(r, timeout=30).read())
    return sum(1 for x in rows if x.get("state") in ("work", "queued"))


calm = 0
while calm < 3:                      # ketma-ket 3 marta (~1.5 daq) bo'sh - boblar orasidagi tanaffus aldamasin
    try:
        n = busy()
    except Exception as exc:
        print("darvoza javob bermadi:", exc); n = 1
    calm = calm + 1 if n == 0 else 0
    print(time.strftime("%H:%M:%S"), "band boblar:", n, flush=True)
    time.sleep(30)
print("hovuz bo'sh - joylanmoqda")
sys.exit(subprocess.run([sys.executable, str(H / "setup.py"), sys.argv[1]]).returncode)
