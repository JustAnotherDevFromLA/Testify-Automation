"""Behave environment hooks — browser lifecycle, page object setup, and failure handling."""

import logging
import os
from datetime import datetime

import allure
from playwright.sync_api import sync_playwright

import config
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.responsive_page import ResponsivePage

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")

# ── Logging Setup ───────────────────────────────────────────────────────────
logger = logging.getLogger("testify")


def before_all(context):
    """Launch Playwright and the browser, configure logging."""
    # Configure root logger for the test suite
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    logger.info("Launching %s (headless=%s)", config.BROWSER, config.HEADLESS)
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=config.HEADLESS)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def after_all(context):
    """Shut down the browser and Playwright."""
    context.browser.close()
    context.playwright.stop()
    logger.info("Browser closed")


def before_scenario(context, scenario):
    """Create an isolated browser context and page for each scenario."""
    logger.debug("▶ Starting: %s", scenario.name)
    context.browser_context = context.browser.new_context(
        viewport={"width": config.VIEWPORT_WIDTH, "height": config.VIEWPORT_HEIGHT},
    )
    context.browser_context.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
    context.page = context.browser_context.new_page()
    context.home_page = HomePage(context.page)
    context.contact_page = ContactPage(context.page)
    context.responsive_page = ResponsivePage(context.page)


def after_scenario(context, scenario):
    """Capture failure screenshots and clean up the browser context."""
    try:
        if scenario.status == "failed":
            _capture_failure_screenshot(context, scenario)
    finally:
        # Guarantee cleanup even if screenshot capture fails
        context.page.close()
        context.browser_context.close()
        logger.debug("◼ Finished: %s [%s]", scenario.name, scenario.status)


def _capture_failure_screenshot(context, scenario):
    """Save a timestamped screenshot and attach it to the Allure report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = scenario.name.replace(" ", "_").replace("-", "")[:50]
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}_{timestamp}.png")

    screenshot_bytes = context.page.screenshot(path=screenshot_path)
    allure.attach(
        screenshot_bytes,
        name="Failure Screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    logger.warning("📸 Screenshot saved: %s", screenshot_path)
