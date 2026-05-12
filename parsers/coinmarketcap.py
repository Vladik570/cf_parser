from playwright.async_api import async_playwright, Page

async def collect_token_links(page: Page, start_url: str) -> list[str]:

