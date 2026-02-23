"""Base page object with shared navigation, retry, and assertion helpers."""

import logging
import time

from playwright.sync_api import Page, expect

import config

logger = logging.getLogger("testify")


class BasePage:
    """Base class for all page objects. Provides navigation with automatic
    retry logic, visibility assertions, and viewport checks."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str, wait_until: str = "networkidle", retries: int | None = None) -> None:
        """Navigate to *url*, retrying on transient network errors.

        Args:
            url: The URL to navigate to.
            wait_until: When to consider navigation succeeded ("domcontentloaded", "load", "networkidle").
            retries: Override retry count (defaults to ``config.RETRY_ATTEMPTS``).
        """
        max_attempts = retries if retries is not None else config.RETRY_ATTEMPTS
        for attempt in range(max_attempts):
            try:
                self.page.goto(url, timeout=config.NAVIGATION_TIMEOUT_MS, wait_until=wait_until)
                return
            except Exception as e:
                if attempt < max_attempts - 1 and "net::ERR_" in str(e):
                    logger.warning(
                        "Navigation attempt %d/%d failed (%s) — retrying in %ds",
                        attempt + 1,
                        max_attempts,
                        str(e).split("\n")[0],
                        config.RETRY_DELAY_S,
                    )
                    time.sleep(config.RETRY_DELAY_S)
                else:
                    raise

    def verify_title(self, title: str) -> None:
        """Assert the page title matches *title*."""
        expect(self.page).to_have_title(title)

    def is_visible(self, selector: str) -> None:
        """Assert the first element matching *selector* is visible."""
        expect(self.page.locator(selector).first).to_be_visible()

    def is_in_viewport(self, selector: str) -> None:
        """Assert the first element matching *selector* is in the viewport."""
        expect(self.page.locator(selector).first).to_be_in_viewport()

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url
