from behave import when, then

# --- Contact Form Steps ---

@when('the user navigates to the contact section')
def step_navigate_to_contact(context):
    context.contact_page.navigate_to_contact()

@then('the contact form should be visible')
def step_verify_form_visible(context):
    context.contact_page.verify_form_visible()

@then('the "{field_name}" field should be visible')
def step_verify_field_visible(context, field_name):
    context.contact_page.verify_field_visible(field_name)

@then('the Send Message button should be visible')
def step_verify_send_btn_visible(context):
    context.contact_page.verify_send_button_visible()

@when('the user fills in the contact form with:')
def step_fill_contact_form(context):
    context.form_data = {}
    for row in context.table:
        field, value = row['Field'], row['Value']
        context.contact_page.fill_field(field, value)
        context.form_data[field] = value

@then('all contact form fields should retain their values')
def step_verify_all_fields_retained(context):
    for field, value in context.form_data.items():
        context.contact_page.verify_field_has_value(field, value)

@when('the user clicks the Send Message button')
def step_click_send_message(context):
    context.contact_page.click_send_message()

@then('the browser should show validation on the "{field_name}" field')
def step_verify_validation(context, field_name):
    context.contact_page.verify_field_validation_active(field_name)

@when('the user fills in the "{field_name}" field with "{value}"')
def step_fill_single_field(context, field_name, value):
    context.contact_page.fill_field(field_name, value)

@then('the email field should show a format validation error')
def step_verify_email_format_validation(context):
    context.contact_page.verify_email_type_validation()
