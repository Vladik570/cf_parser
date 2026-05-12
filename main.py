from playwright.async_api import async_playwright
import asyncio
from config import START_URL
from utils.html_saver import save_page_html
from parsers.coinmarketcap import collect_token_links_from_file


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = await browser.new_page()
        await page.goto(START_URL)
        links = collect_token_links_from_file(
            "saved_pages/coinmarketcap.html"
        )

        for link in links:
            print(link)

        await save_page_html(page, "coinmarketcap.html")
        input("press enter to close")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())