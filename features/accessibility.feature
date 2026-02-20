@accessibility
Feature: Accessibility Suite for artasheskocharyan.com

  Background:
    Given the user navigates to the home page

  @a11y
  Scenario: TC-A01 - All images have alt text
    Then every image on the page should have alt text

  @a11y
  Scenario: TC-A02 - Heading hierarchy is correct
    Then there should be exactly 1 h1 element
    And headings should follow a logical order

  @a11y
  Scenario: TC-A03 - Page has a lang attribute
    Then the html element should have a lang attribute

  @a11y
  Scenario: TC-A04 - Interactive elements are keyboard accessible
    Then all links should have non-empty href attributes
    And the submit button should be focusable

  @a11y
  Scenario: TC-A05 - Color contrast and text readability
    Then the body text should have a minimum font size of 12px
