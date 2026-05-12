from playwright.async_api import async_playwright
import asyncio
from config import START_URL

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = await browser.new_page()
        await page.goto(START_URL)
        input("press enter to close")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())