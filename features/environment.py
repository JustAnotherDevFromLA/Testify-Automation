import os
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
from pages.contact_page import ContactPage
from pages.responsive_page import ResponsivePage

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports', 'screenshots')

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def after_all(context):
    context.browser.close()
    context.playwright.stop()

def before_scenario(context, scenario):
    context.context = context.browser.new_context(viewport={"width": 1280, "height": 720})
    context.page = context.context.new_page()
    context.home_page = HomePage(context.page)
    context.contact_page = ContactPage(context.page)
    context.responsive_page = ResponsivePage(context.page)

def after_scenario(context, scenario):
    if scenario.status == "failed":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = scenario.name.replace(" ", "_").replace("-", "")[:50]
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}_{timestamp}.png")
        screenshot_bytes = context.page.screenshot(path=screenshot_path)
        allure.attach(screenshot_bytes, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
        print(f"\n📸 Screenshot saved: {screenshot_path}")
    context.page.close()
    context.context.close()
