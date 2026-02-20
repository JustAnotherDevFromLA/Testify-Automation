from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class HomePage(BasePage):
    URL = "https://artasheskocharyan.com"

    # Navigation Selectors
    NAV_LINKS = {
        "About Me": 'a[href="#about"]',
        "Portfolio": 'a[href="#portfolio"]',
        "Resume": 'a[href="#resume"]',
        "Get in Touch": 'a[href="#contact"]'
    }

    HEADINGS = {
        "About Me": '#about h2',
        "Portfolio": '#portfolio h2',
        "Resume": '#resume h2',
        "Get in Touch": '#contact h2'
    }

    # Social Links
    SOCIAL_LINKS = {
        "Twitter": 'a[href*="twitter.com/"], a[href*="x.com/"]',
        "GitHub": 'a[href*="github.com/"]',
        "LinkedIn": 'a[href*="linkedin.com/in/"]'
    }

    SOCIAL_URLS = {
        "Twitter": "twitter.com/expertfrogger",
        "GitHub": "github.com/JustAnotherDevFromLA",
        "LinkedIn": "linkedin.com/in/artashes-kocharyan"
    }

    # Hero Section
    HERO_PROFILE_IMAGE = '#profile .image.avi img'
    HERO_TAGLINE = '#top h2, #intro h2, .blurb h2'
    SIDEBAR_NAME = 'h1#title'
    SIDEBAR_TITLE = '#profile p'
    HERO_PORTFOLIO_BTN = '#top a.button[href="#portfolio"], #intro a.button[href="#portfolio"]'
    PORTFOLIO_HEADING = '#portfolio h2'

    # About Me
    ABOUT_SECTION = '#about'
    ABOUT_TEXT = '#about p'

    # Portfolio
    PORTFOLIO_ITEMS = '#portfolio article'
    PORTFOLIO_ITEM_TITLES = '#portfolio article h3'
    PORTFOLIO_ITEM_LINKS = '#portfolio article a'

    # Resume
    PDF_VIEWER = '#resume iframe, #resume embed, #resume object, #resume .pdf-viewer'
    RESUME_DOWNLOAD_LINK = '#resume a[href$=".pdf"]'

    # Footer
    FOOTER_COPYRIGHT = '#footer .copyright, footer .copyright, #copyright'

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_home(self):
        self.navigate(self.URL)

    # Navigation
    def click_nav_link(self, link_name: str):
        self.page.click(self.NAV_LINKS[link_name])

    def verify_heading_visible(self, heading_text: str):
        expect(self.page.locator(self.HEADINGS[heading_text])).to_contain_text(heading_text)

    # Social Links
    def verify_social_link_visible(self, platform: str):
        expect(self.page.locator(self.SOCIAL_LINKS[platform]).first).to_be_visible()

    def verify_social_link_url(self, platform: str):
        href = self.page.locator(self.SOCIAL_LINKS[platform]).first.get_attribute("href")
        expected_fragment = self.SOCIAL_URLS[platform]
        assert expected_fragment in href, f"Expected {platform} link to contain '{expected_fragment}', got '{href}'"

    # Hero Section
    def verify_profile_image_visible(self):
        expect(self.page.locator(self.HERO_PROFILE_IMAGE).first).to_be_visible()

    def verify_tagline_visible(self):
        expect(self.page.locator(self.HERO_TAGLINE).first).to_be_visible()

    def verify_sidebar_name_visible(self, name: str):
        expect(self.page.locator(self.SIDEBAR_NAME).first).to_contain_text(name)

    def click_hero_portfolio_button(self):
        self.page.locator(self.HERO_PORTFOLIO_BTN).first.click()

    def verify_portfolio_in_viewport(self):
        expect(self.page.locator(self.PORTFOLIO_HEADING)).to_be_in_viewport()

    # About Me
    def verify_about_contains_text(self, text: str):
        expect(self.page.locator(self.ABOUT_TEXT).first).to_contain_text(text)

    # Portfolio
    def verify_portfolio_item_count(self, count: int):
        expect(self.page.locator(self.PORTFOLIO_ITEMS)).to_have_count(count)

    def verify_portfolio_item_title_visible(self, title: str):
        expect(self.page.locator(self.PORTFOLIO_ITEM_TITLES).filter(has_text=title).first).to_be_visible()

    def get_portfolio_item_link(self, title: str):
        article = self.page.locator(self.PORTFOLIO_ITEMS).filter(has_text=title).first
        return article.locator("a").first.get_attribute("href")

    # Resume
    def verify_pdf_viewer_visible(self):
        expect(self.page.locator(self.PDF_VIEWER).first).to_be_visible()

    def verify_resume_download_link(self):
        locator = self.page.locator(self.RESUME_DOWNLOAD_LINK).first
        expect(locator).to_be_visible()
        href = locator.get_attribute("href")
        assert href and ".pdf" in href, f"Expected resume link to point to a PDF, got '{href}'"

    # Footer
    def verify_footer_copyright(self, text: str):
        expect(self.page.locator(self.FOOTER_COPYRIGHT).first).to_contain_text(text)

    # Meta Tags
    def verify_meta_tag(self, name: str, attr: str = "name"):
        content = self.page.locator(f'meta[{attr}="{name}"]').get_attribute("content")
        assert content and len(content) > 0, f"Meta tag '{name}' is missing or empty"

    def get_meta_content(self, name: str, attr: str = "name"):
        return self.page.locator(f'meta[{attr}="{name}"]').get_attribute("content")
