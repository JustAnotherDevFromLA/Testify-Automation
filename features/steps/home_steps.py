from behave import given, then, when
from playwright.sync_api import expect


@given("the user navigates to the home page")
def step_navigate_to_home(context):
    context.home_page.navigate_home()


@then('the page title should be "{title_text}"')
def step_verify_page_title(context, title_text):
    context.home_page.verify_title(title_text)


@when('the user clicks on the "{link_name}" link')
def step_click_link(context, link_name):
    context.home_page.click_nav_link(link_name)


@then('the "{heading_text}" heading should be visible')
def step_verify_heading_visible(context, heading_text):
    context.home_page.verify_heading_visible(heading_text)


@then("the {platform} link should be visible")
def step_verify_social_link(context, platform):
    context.home_page.verify_social_link_visible(platform)


@then("the PDF viewer should be visible")
def step_verify_pdf_viewer(context):
    context.home_page.verify_pdf_viewer_visible()


@when("the user clicks the Portfolio button in the hero section")
def step_click_hero_portfolio_btn(context):
    context.home_page.click_hero_portfolio_button()


@then("the portfolio section should be in the viewport")
def step_verify_portfolio_in_viewport(context):
    context.home_page.verify_portfolio_in_viewport()


# --- Hero Section (TC-009) ---


@then("the profile image should be visible")
def step_verify_profile_image(context):
    context.home_page.verify_profile_image_visible()


@then('the sidebar should display the name "{name}"')
def step_verify_sidebar_name(context, name):
    context.home_page.verify_sidebar_name_visible(name)


@then("the hero tagline should be visible")
def step_verify_tagline(context):
    context.home_page.verify_tagline_visible()


# --- About Me (TC-010) ---


@then('the about section should contain "{text}"')
def step_verify_about_text(context, text):
    context.home_page.verify_about_contains_text(text)


# --- Resume (TC-013) ---


@then("the resume download link should point to a PDF")
def step_verify_resume_link(context):
    context.home_page.verify_resume_download_link()


# --- Footer (TC-014) ---


@then('the footer should contain "{text}"')
def step_verify_footer(context, text):
    context.home_page.verify_footer_copyright(text)


# --- Social Link URLs (TC-015) ---


@then("the {platform} link should point to the correct URL")
def step_verify_social_url(context, platform):
    context.home_page.verify_social_link_url(platform)


# --- SEO Meta Tags (TC-017) ---


@then('the meta tag "{name}" should be present')
def step_verify_meta_tag(context, name):
    context.home_page.verify_meta_tag(name)


@then('the og meta tag "{name}" should be present')
def step_verify_og_meta_tag(context, name):
    context.home_page.verify_meta_tag(name, attr="property")


# --- Smooth scroll (TC-020) ---


@then('the "{heading_text}" heading should be in the viewport')
def step_verify_heading_in_viewport(context, heading_text):
    heading = context.home_page.HEADINGS.get(heading_text)
    assert heading, f"No heading mapping for '{heading_text}'"
    expect(context.page.locator(heading)).to_be_in_viewport()


# --- Email mailto link (TC-021) ---


@then("the {platform} link should be a mailto link")
def step_verify_mailto_link(context, platform):
    selector = context.home_page.SOCIAL_LINKS.get(platform)
    assert selector, f"No selector for '{platform}'"
    href = context.page.locator(selector).first.get_attribute("href")
    assert href and href.startswith("mailto:"), f"Expected mailto link, got '{href}'"


# --- Resume iframe (TC-022) ---


@then("the resume iframe should point to a PDF file")
def step_verify_resume_iframe(context):
    context.home_page.verify_resume_iframe_src()
