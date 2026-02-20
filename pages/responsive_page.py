from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class ResponsivePage(BasePage):
    """Page object for testing responsive/mobile behavior."""

    URL = "https://artasheskocharyan.com"

    SIDEBAR = '#header'
    HERO_TAGLINE = '#top h2, #intro h2, .blurb h2'

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_home(self):
        self.navigate(self.URL)
        self.page.wait_for_load_state("networkidle")

    def verify_sidebar_not_in_viewport(self):
        """On mobile, the sidebar is positioned off-screen via CSS."""
        is_off_screen = self.page.locator(self.SIDEBAR).evaluate(
            """el => {
                const rect = el.getBoundingClientRect();
                return rect.right <= 0 || rect.left >= window.innerWidth;
            }"""
        )
        assert is_off_screen, "Expected sidebar to be off-screen on mobile viewport"

    def verify_content_fills_viewport(self):
        """On mobile, the main content should fill the full width."""
        main_width = self.page.locator('#main, main, .wrapper').first.evaluate(
            "el => el.getBoundingClientRect().width"
        )
        viewport_width = self.page.evaluate("window.innerWidth")
        # Content should use at least 90% of viewport width on mobile
        assert main_width >= viewport_width * 0.9, (
            f"Expected content to fill viewport ({viewport_width}px), but it's {main_width}px"
        )
