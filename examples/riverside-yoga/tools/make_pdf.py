"""Print an HTML document to PDF (and optionally a PNG preview) with a headless Chromium browser.

    python tools/make_pdf.py                                   # docs/sales/Quote-brief.html → .pdf
    python tools/make_pdf.py docs/infrastructure/Infrastructure.html
    python tools/make_pdf.py docs/sales/Quote-brief.html --png  # also a first-screen PNG preview

Uses Chrome, Edge, Chromium or Brave, whichever it finds; set CHROME=/path/to/browser
to choose. Works on Windows, macOS and Linux.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "docs" / "sales" / "Quote-brief.html"

CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
ON_PATH = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
           "microsoft-edge", "msedge", "brave-browser", "chrome"]


def browser():
    for c in CANDIDATES:
        if c and Path(c).is_file():
            return c
    for name in ON_PATH:
        found = shutil.which(name)
        if found:
            return found
    sys.exit("No Chrome, Edge, Chromium or Brave found. Install one, or set CHROME=/path/to/browser.")


def run(exe, *args):
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                        f"--user-data-dir={profile}", "--virtual-time-budget=8000", *args],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, timeout=120)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    html = Path(args[0]).resolve() if args else DEFAULT
    if not html.is_file():
        sys.exit(f"Not found: {html}")
    exe = browser()
    pdf = html.with_suffix(".pdf")
    if pdf.exists():
        pdf.unlink()
    run(exe, "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri())
    if not pdf.is_file():
        sys.exit("PDF not created: try another browser with CHROME=/path/to/browser.")
    print(f"Written {pdf}")
    if "--png" in sys.argv:
        png = html.with_suffix(".png")
        run(exe, "--hide-scrollbars", "--window-size=1280,1600", f"--screenshot={png}", html.as_uri())
        print(f"Written {png}" if png.is_file() else "PNG not created.")


if __name__ == "__main__":
    main()
