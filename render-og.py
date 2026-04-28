"""Convert OG-image SVG templates to PNG via Playwright (Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SVGS = ["og-portal.svg", "og-licensing.svg", "og-compliance.svg", "og-wizard.svg"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630})
    for svg in SVGS:
        src = HERE / svg
        dst = HERE / src.with_suffix(".png").name
        page.goto(src.resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(dst), full_page=False, omit_background=False, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        print(f"OK -> {dst.name} ({dst.stat().st_size:,} bytes)")
    browser.close()
