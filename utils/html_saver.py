from pathlib import Path
from playwright.async_api import Page

from config import SAVED_PAGES_DIR


async def save_page_html(page: Page, filename: str) -> Path:
    SAVED_PAGES_DIR.mkdir(exist_ok=True)
    html = await page.content()
    file_path = SAVED_PAGES_DIR / filename
    file_path.write_text(html, encoding="utf-8")

    return file_path
