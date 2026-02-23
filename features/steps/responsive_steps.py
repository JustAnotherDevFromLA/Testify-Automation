from behave import given, then


@given("the user navigates to the home page in mobile view")
def step_navigate_mobile(context):
    # Close the default desktop context and create a fresh mobile one
    context.page.close()
    context.browser_context.close()
    context.browser_context = context.browser.new_context(viewport={"width": 375, "height": 667})
    context.page = context.browser_context.new_page()
    # Re-create page objects with the new mobile page
    from pages.home_page import HomePage
    from pages.responsive_page import ResponsivePage

    context.home_page = HomePage(context.page)
    context.responsive_page = ResponsivePage(context.page)
    context.responsive_page.navigate_home()


@then("the sidebar should be hidden")
def step_verify_sidebar_hidden(context):
    context.responsive_page.verify_sidebar_not_in_viewport()
