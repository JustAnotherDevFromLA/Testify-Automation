from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class ContactPage(BasePage):
    # Selectors
    CONTACT_NAV_LINK = 'a[href="#contact"]'
    CONTACT_FORM = '#contact form'

    FIELDS = {
        "Full Name": 'input[name="name"]',
        "Email Address": 'input[name="email"]',
        "Subject": 'input[name="subject"]',
        "Phone Number": 'input[name="number"]',
        "Message": 'textarea[name="message"]',
    }

    SEND_MESSAGE_BTN = 'input[type="submit"][value="Send Message"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_contact(self):
        self.page.click(self.CONTACT_NAV_LINK)

    def verify_form_visible(self):
        expect(self.page.locator(self.CONTACT_FORM)).to_be_visible()

    def verify_field_visible(self, field_name: str):
        expect(self.page.locator(self.FIELDS[field_name])).to_be_visible()

    def verify_send_button_visible(self):
        expect(self.page.locator(self.SEND_MESSAGE_BTN)).to_be_visible()

    def fill_field(self, field_name: str, value: str):
        self.page.locator(self.FIELDS[field_name]).fill(value)

    def verify_field_has_value(self, field_name: str, value: str):
        expect(self.page.locator(self.FIELDS[field_name])).to_have_value(value)

    def click_send_message(self):
        self.page.locator(self.SEND_MESSAGE_BTN).click()

    def verify_field_validation_active(self, field_name: str):
        """Verify the browser's HTML5 validation is triggered on a required field."""
        locator = self.page.locator(self.FIELDS[field_name])
        # The field should be the active validation target after failed submission
        validity = locator.evaluate("el => !el.validity.valid && el.validationMessage !== ''")
        assert validity, f"Expected HTML5 validation on '{field_name}' but it was valid"

    def verify_email_type_validation(self):
        """Verify the browser rejects an invalid email format via type=email validation."""
        locator = self.page.locator(self.FIELDS["Email Address"])
        validity = locator.evaluate("el => !el.validity.valid && el.validity.typeMismatch")
        assert validity, "Expected email type validation error but field was valid"
