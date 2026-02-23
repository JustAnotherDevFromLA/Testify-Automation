"""Page object for the main site: navigation, hero, about, portfolio, resume, footer, and meta."""

from typing import ClassVar

from playwright.sync_api import Page, expect

import config
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object encapsulating all interactions with the home page of
    artasheskocharyan.com.  Selectors are defined as class-level constants
    and methods expose atomic, reusable actions."""

    URL: str = config.BASE_URL

    # ── Navigation ──────────────────────────────────────────────────────
    NAV_LINKS: ClassVar[dict[str, str]] = {
        "About Me": 'a[href="#about"]',
        "Portfolio": 'a[href="#portfolio"]',
        "Resume": 'a[href="#resume"]',
        "Get in Touch": 'a[href="#contact"]',
    }

    HEADINGS: ClassVar[dict[str, str]] = {
        "About Me": "#about h2",
        "Portfolio": "#portfolio h2",
        "Resume": "#resume h2",
        "Get in Touch": "#contact h2",
    }

    # ── Social Links ────────────────────────────────────────────────────
    SOCIAL_LINKS: ClassVar[dict[str, str]] = {
        "Twitter": 'a[href*="twitter.com/"], a[href*="x.com/"]',
        "GitHub": 'a[href*="github.com/"]',
        "LinkedIn": 'a[href*="linkedin.com/in/"]',
        "Email": 'a[href^="mailto:"]',
    }

    SOCIAL_URLS: ClassVar[dict[str, str]] = {
        "Twitter": "twitter.com/expertfrogger",
        "GitHub": "github.com/JustAnotherDevFromLA",
        "LinkedIn": "linkedin.com/in/artashes-kocharyan",
        "Email": "mailto:",
    }

    # ── Hero Section ────────────────────────────────────────────────────
    HERO_PROFILE_IMAGE: str = "#profile .image.avi img"
    HERO_TAGLINE: str = "#top h2, #intro h2, .blurb h2"
    SIDEBAR_NAME: str = "h1#title"
    SIDEBAR_TITLE: str = "#profile p"
    HERO_PORTFOLIO_BTN: str = '#top a.button[href="#portfolio"], #intro a.button[href="#portfolio"]'
    PORTFOLIO_HEADING: str = "#portfolio h2"

    # ── About Me ────────────────────────────────────────────────────────
    ABOUT_SECTION: str = "#about"
    ABOUT_TEXT: str = "#about p"

    # ── Portfolio ───────────────────────────────────────────────────────
    PORTFOLIO_ITEMS: str = "#portfolio article"
    PORTFOLIO_ITEM_TITLES: str = "#portfolio article h3"
    PORTFOLIO_ITEM_LINKS: str = "#portfolio article a"
    PORTFOLIO_ITEM_IMAGES: str = "#portfolio article img"

    # ── Resume ──────────────────────────────────────────────────────────
    PDF_VIEWER: str = "#resume iframe, #resume embed, #resume object, #resume .pdf-viewer"
    RESUME_IFRAME: str = "#resume iframe"
    RESUME_DOWNLOAD_LINK: str = '#resume a[href$=".pdf"]'

    # ── Footer ──────────────────────────────────────────────────────────
    FOOTER_COPYRIGHT: str = "#footer .copyright, footer .copyright, #copyright"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Navigation ──────────────────────────────────────────────────────

    def navigate_home(self) -> None:
        """Navigate to the home page."""
        self.navigate(self.URL)

    def click_nav_link(self, link_name: str) -> None:
        """Click a navigation link by its display name."""
        self.page.click(self.NAV_LINKS[link_name])

    def verify_heading_visible(self, heading_text: str) -> None:
        """Assert a section heading is visible and contains *heading_text*."""
        expect(self.page.locator(self.HEADINGS[heading_text])).to_contain_text(heading_text)

    # ── Social Links ────────────────────────────────────────────────────

    def verify_social_link_visible(self, platform: str) -> None:
        """Assert the social link for *platform* is visible."""
        expect(self.page.locator(self.SOCIAL_LINKS[platform]).first).to_be_visible()

    def verify_social_link_url(self, platform: str) -> None:
        """Assert the social link href contains the expected URL fragment."""
        href = self.page.locator(self.SOCIAL_LINKS[platform]).first.get_attribute("href")
        expected_fragment = self.SOCIAL_URLS[platform]
        assert expected_fragment in href, f"Expected {platform} link to contain '{expected_fragment}', got '{href}'"

    # ── Hero Section ────────────────────────────────────────────────────

    def verify_profile_image_visible(self) -> None:
        """Assert the hero profile image is visible."""
        expect(self.page.locator(self.HERO_PROFILE_IMAGE).first).to_be_visible()

    def verify_tagline_visible(self) -> None:
        """Assert the hero tagline is visible."""
        expect(self.page.locator(self.HERO_TAGLINE).first).to_be_visible()

    def verify_sidebar_name_visible(self, name: str) -> None:
        """Assert the sidebar displays *name*."""
        expect(self.page.locator(self.SIDEBAR_NAME).first).to_contain_text(name)

    def click_hero_portfolio_button(self) -> None:
        """Click the CTA button in the hero section."""
        self.page.locator(self.HERO_PORTFOLIO_BTN).first.click()

    def verify_portfolio_in_viewport(self) -> None:
        """Assert the portfolio heading has scrolled into the viewport."""
        expect(self.page.locator(self.PORTFOLIO_HEADING)).to_be_in_viewport()

    # ── About Me ────────────────────────────────────────────────────────

    def verify_about_contains_text(self, text: str) -> None:
        """Assert the about section contains *text*."""
        expect(self.page.locator(self.ABOUT_TEXT).first).to_contain_text(text)

    # ── Portfolio ───────────────────────────────────────────────────────

    def verify_portfolio_item_count(self, count: int) -> None:
        """Assert the number of portfolio items matches *count*."""
        expect(self.page.locator(self.PORTFOLIO_ITEMS)).to_have_count(count)

    def verify_portfolio_item_title_visible(self, title: str) -> None:
        """Assert a portfolio item with *title* is visible."""
        expect(self.page.locator(self.PORTFOLIO_ITEM_TITLES).filter(has_text=title).first).to_be_visible()

    def get_portfolio_item_link(self, title: str) -> str:
        """Return the href of the link inside the portfolio item with *title*."""
        article = self.page.locator(self.PORTFOLIO_ITEMS).filter(has_text=title).first
        return article.locator("a").first.get_attribute("href")

    def verify_portfolio_item_images(self) -> None:
        """Assert every portfolio item has a visible image with non-zero dimensions."""
        images = self.page.locator(self.PORTFOLIO_ITEM_IMAGES)
        count = images.count()
        assert count > 0, "No portfolio item images found"
        for i in range(count):
            expect(images.nth(i)).to_be_visible()

    # ── Resume ──────────────────────────────────────────────────────────

    def verify_pdf_viewer_visible(self) -> None:
        """Assert the PDF viewer element is visible in the Resume section."""
        expect(self.page.locator(self.PDF_VIEWER).first).to_be_visible()

    def verify_resume_download_link(self) -> None:
        """Assert a visible download link pointing to a PDF exists."""
        locator = self.page.locator(self.RESUME_DOWNLOAD_LINK).first
        expect(locator).to_be_visible()
        href = locator.get_attribute("href")
        assert href and ".pdf" in href, f"Expected resume link to point to a PDF, got '{href}'"

    def verify_resume_iframe_src(self) -> None:
        """Assert the resume iframe's src attribute points to a PDF file."""
        locator = self.page.locator(self.RESUME_IFRAME).first
        expect(locator).to_be_visible()
        src = locator.get_attribute("src")
        assert src and ".pdf" in src, f"Expected resume iframe to load a PDF, got '{src}'"

    # ── Footer ──────────────────────────────────────────────────────────

    def verify_footer_copyright(self, text: str) -> None:
        """Assert the footer copyright contains *text*."""
        expect(self.page.locator(self.FOOTER_COPYRIGHT).first).to_contain_text(text)

    # ── Meta Tags ───────────────────────────────────────────────────────

    def verify_meta_tag(self, name: str, attr: str = "name") -> None:
        """Assert a meta tag with the given *name* attribute has non-empty content."""
        content = self.page.locator(f'meta[{attr}="{name}"]').get_attribute("content")
        assert content and len(content) > 0, f"Meta tag '{name}' is missing or empty"

    def get_meta_content(self, name: str, attr: str = "name") -> str | None:
        """Return the content attribute of a meta tag."""
        return self.page.locator(f'meta[{attr}="{name}"]').get_attribute("content")
