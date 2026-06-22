"""Render the AML/CTF Playbook HTML to a branded PDF via Playwright (Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SRC = HERE / "playbook-v2.html"
DST = HERE.parent / "aml-playbook-dasp-el-salvador.pdf"  # publish straight to the site-linked PDF

url = SRC.resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")
    page.pdf(
        path=str(DST),
        format="A4",
        print_background=True,
        prefer_css_page_size=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    browser.close()

print(f"OK -> {DST}")
print(f"Size: {DST.stat().st_size:,} bytes")
