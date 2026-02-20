"""Page object for the contact form section."""
from typing import ClassVar

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Encapsulates interactions with the contact form: field filling,
    button clicking, and HTML5 validation checks."""

    # ── Selectors ───────────────────────────────────────────────────────
    CONTACT_NAV_LINK: str = 'a[href="#contact"]'
    CONTACT_FORM: str = "#contact form"

    FIELDS: ClassVar[dict[str, str]] = {
        "Full Name": 'input[name="name"]',
        "Email Address": 'input[name="email"]',
        "Subject": 'input[name="subject"]',
        "Phone Number": 'input[name="number"]',
        "Message": 'textarea[name="message"]',
    }

    SEND_MESSAGE_BTN: str = 'input[type="submit"][value="Send Message"]'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate_to_contact(self) -> None:
        """Click the in-page link to scroll to the contact section."""
        self.page.click(self.CONTACT_NAV_LINK)

    def verify_form_visible(self) -> None:
        """Assert the contact form is visible."""
        expect(self.page.locator(self.CONTACT_FORM)).to_be_visible()

    def verify_field_visible(self, field_name: str) -> None:
        """Assert a specific form field is visible."""
        expect(self.page.locator(self.FIELDS[field_name])).to_be_visible()

    def verify_send_button_visible(self) -> None:
        """Assert the Send Message button is visible."""
        expect(self.page.locator(self.SEND_MESSAGE_BTN)).to_be_visible()

    def fill_field(self, field_name: str, value: str) -> None:
        """Fill a form field with a value."""
        self.page.locator(self.FIELDS[field_name]).fill(value)

    def verify_field_has_value(self, field_name: str, value: str) -> None:
        """Assert a form field retains the expected value."""
        expect(self.page.locator(self.FIELDS[field_name])).to_have_value(value)

    def click_send_message(self) -> None:
        """Click the Send Message submit button."""
        self.page.locator(self.SEND_MESSAGE_BTN).click()

    def verify_field_validation_active(self, field_name: str) -> None:
        """Verify the browser's HTML5 validation is triggered on a required field."""
        locator = self.page.locator(self.FIELDS[field_name])
        validity = locator.evaluate("el => !el.validity.valid && el.validationMessage !== ''")
        assert validity, f"Expected HTML5 validation on '{field_name}' but it was valid"

    def verify_email_type_validation(self) -> None:
        """Verify the browser rejects an invalid email format via type=email validation."""
        locator = self.page.locator(self.FIELDS["Email Address"])
        validity = locator.evaluate("el => !el.validity.valid && el.validity.typeMismatch")
        assert validity, "Expected email type validation error but field was valid"
