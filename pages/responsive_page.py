"""Page object for testing responsive/mobile behavior."""

from playwright.sync_api import Page

import config
from pages.base_page import BasePage


class ResponsivePage(BasePage):
    """Page object for verifying the site renders correctly on mobile
    viewports (sidebar hidden, content fills width)."""

    URL: str = config.BASE_URL

    SIDEBAR: str = "#header"
    HERO_TAGLINE: str = "#top h2, #intro h2, .blurb h2"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate_home(self) -> None:
        """Navigate to the home page and wait for network idle."""
        self.navigate(self.URL)
        self.page.wait_for_load_state("networkidle")

    def verify_sidebar_not_in_viewport(self) -> None:
        """Assert the sidebar is positioned off-screen on mobile."""
        is_off_screen = self.page.locator(self.SIDEBAR).evaluate(
            """el => {
                const rect = el.getBoundingClientRect();
                return rect.right <= 0 || rect.left >= window.innerWidth;
            }"""
        )
        assert is_off_screen, "Expected sidebar to be off-screen on mobile viewport"

    def verify_content_fills_viewport(self) -> None:
        """Assert the main content fills at least 90% of the viewport width."""
        main_width = self.page.locator("#main, main, .wrapper").first.evaluate("el => el.getBoundingClientRect().width")
        viewport_width = self.page.evaluate("window.innerWidth")
        assert main_width >= viewport_width * 0.9, (
            f"Expected content to fill viewport ({viewport_width}px), but it's {main_width}px"
        )
