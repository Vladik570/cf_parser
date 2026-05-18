from playwright.async_api import async_playwright
import asyncio
from config import START_URL
from utils.html_saver import save_page_html
from parsers.coinmarketcap import collect_token_links_from_file, collect_token_info


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = await browser.new_page()
        await page.goto(START_URL)

        await page.wait_for_selector("table tbody tr", timeout=15000)
        await page.wait_for_timeout(3000)
        await save_page_html(page, "coinmarketcap.html")
        links = collect_token_links_from_file(
            "saved_pages/coinmarketcap.html"
        )

        for index, link in enumerate(links, start=1):
            print(f'Open {index}: {link}')

            await page.goto(link, wait_until='domcontentloaded')
            filename = f"coin{index}.html"

            await save_page_html(page, filename)
            info = collect_token_info(f"saved_pages/{filename}")

            print(info["name"])
            print(info["ticker"])
            print(info["website"])
            print(info["socials"])

        input("press enter to close")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())