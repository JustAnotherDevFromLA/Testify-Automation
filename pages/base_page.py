import time
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str, retries: int = 3):
        for attempt in range(retries):
            try:
                self.page.goto(url)
                return
            except Exception as e:
                if attempt < retries - 1 and "net::ERR_" in str(e):
                    time.sleep(2)
                else:
                    raise

    def verify_title(self, title: str):
        expect(self.page).to_have_title(title)

    def is_visible(self, selector: str):
        expect(self.page.locator(selector).first).to_be_visible()

    def is_in_viewport(self, selector: str):
        expect(self.page.locator(selector).first).to_be_in_viewport()
