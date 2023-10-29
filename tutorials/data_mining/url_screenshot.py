import asyncio
import argparse
from pyppeteer import launch

class ScreenshotTaker:
    def __init__(self, url, filename, delay=5000):
        self.browser = None
        self.url = url
        self.filename = filename
        self.delay = delay

    async def start_browser(self):
        self.browser = await launch()

    async def stop_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None

    async def take_screenshot(self):
        if not self.browser:
            await self.start_browser()

        page = await self.browser.newPage()
        await page.goto(self.url)

        await page.waitFor(self.delay)

        await page.screenshot({'path': self.filename})
        await page.close()

    def capture(self):
        print('Starting...')
        asyncio.get_event_loop().run_until_complete(self.take_screenshot())
        print('Screenshot successful.')

def main():
    parser = argparse.ArgumentParser(description="Capture screenshots of web pages using Pyppeteer.")
    parser.add_argument("url", type=str, help="URL of the web page to capture")
    parser.add_argument("filename", type=str, help="Filename to save the screenshot as")
    parser.add_argument("--delay", type=int, default=5000, help="Delay in milliseconds to wait for the page to load")
    args = parser.parse_args()

    screenshot_taker = ScreenshotTaker(args.url, args.filename, args.delay)
    try:
        screenshot_taker.capture()
    finally:
        asyncio.get_event_loop().run_until_complete(screenshot_taker.stop_browser())


if __name__ == "__main__":
    main()
