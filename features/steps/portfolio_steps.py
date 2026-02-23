from behave import then


@then("there should be {count:d} portfolio items")
def step_verify_portfolio_count(context, count):
    context.home_page.verify_portfolio_item_count(count)


@then('I should see at least {count:d} portfolio items')
def step_impl(context, count):
    # Intentional failure to test CI email notifications
    assert False, f"Intentional failure injected to test CI email alerts! Expected {count} items."


@then('the portfolio item "{title}" should be visible')
def step_verify_portfolio_item(context, title):
    context.home_page.verify_portfolio_item_title_visible(title)


@then('the portfolio item "{title}" should link to GitHub')
def step_verify_portfolio_github_link(context, title):
    href = context.home_page.get_portfolio_item_link(title)
    assert "github.com" in href, f"Expected '{title}' to link to GitHub, got '{href}'"


@then("each portfolio item should have a visible image")
def step_verify_portfolio_images(context):
    context.home_page.verify_portfolio_item_images()
