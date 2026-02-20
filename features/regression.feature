@regression
Feature: Regression Suite for artasheskocharyan.com

  Background:
    Given the user navigates to the home page

  @smoke @sanity
  Scenario: TC-001 - Page Title verification
    Then the page title should be "Artashes Kocharyan | Software Quality Assurance Engineer"

  @navigation @sanity
  Scenario Outline: TC-002 - Navigation to <Section> works
    When the user clicks on the "<Section>" link
    Then the "<Section>" heading should be visible

    Examples:
      | Section      |
      | About Me     |
      | Portfolio    |
      | Resume       |
      | Get in Touch |

  @links @sanity
  Scenario Outline: TC-003 - <Platform> social link is correct
    Then the <Platform> link should be visible

    Examples:
      | Platform |
      | Twitter  |
      | GitHub   |
      | LinkedIn |

  @ui @sanity
  Scenario: TC-004 - Key content is present in Resume section
    When the user clicks on the "Resume" link
    Then the PDF viewer should be visible

  @ui @smoke @sanity
  Scenario: TC-005 - Hero section CTA works
    When the user clicks the Portfolio button in the hero section
    Then the portfolio section should be in the viewport

  @contact @smoke @sanity
  Scenario: TC-006 - Contact form fields are present
    When the user navigates to the contact section
    Then the contact form should be visible
    And the "Full Name" field should be visible
    And the "Email Address" field should be visible
    And the "Subject" field should be visible
    And the "Phone Number" field should be visible
    And the "Message" field should be visible
    And the Send Message button should be visible

  @contact
  Scenario: TC-007 - User can fill out the contact form
    When the user navigates to the contact section
    And the user fills in the contact form with:
      | Field         | Value                   |
      | Full Name     | Jane Doe                |
      | Email Address | jane@example.com        |
      | Subject       | Test Inquiry            |
      | Phone Number  | 1234567890              |
      | Message       | This is a test message. |
    Then all contact form fields should retain their values

  @contact @validation
  Scenario: TC-008 - Required fields enforce validation
    When the user navigates to the contact section
    And the user clicks the Send Message button
    Then the browser should show validation on the "Full Name" field

  @ui @sanity
  Scenario: TC-009 - Hero section content is displayed
    Then the profile image should be visible
    And the sidebar should display the name "Artashes Kocharyan"
    And the hero tagline should be visible

  @content
  Scenario: TC-010 - About Me section has key content
    When the user clicks on the "About Me" link
    Then the about section should contain "Los Angeles"
    And the about section should contain "Computer Science"
    And the about section should contain "Quality Assurance"

  @portfolio
  Scenario: TC-011 - All portfolio items are displayed
    When the user clicks on the "Portfolio" link
    Then there should be 6 portfolio items
    And the portfolio item "Twitter Bot" should be visible
    And the portfolio item "Process Scheduler Simulator" should be visible
    And the portfolio item "BlackJack Game App" should be visible
    And the portfolio item "Cryoto Currency Platform" should be visible
    And the portfolio item "Ticket Managment Browser Extension" should be visible
    And the portfolio item "Grocery Delivery Web App" should be visible

  @portfolio
  Scenario Outline: TC-012 - Portfolio item "<Project>" links to GitHub
    When the user clicks on the "Portfolio" link
    Then the portfolio item "<Project>" should link to GitHub

    Examples:
      | Project                              |
      | Twitter Bot                          |
      | Process Scheduler Simulator          |
      | Grocery Delivery Web App             |
      | BlackJack Game App                   |
      | Cryoto Currency Platform             |
      | Ticket Managment Browser Extension   |

  @ui
  Scenario: TC-013 - Resume download link is present
    When the user clicks on the "Resume" link
    Then the resume download link should point to a PDF

  @ui @sanity
  Scenario: TC-014 - Footer displays copyright
    Then the footer should contain "Artashes Alex Kocharyan"

  @links
  Scenario Outline: TC-015 - <Platform> links to the correct profile
    Then the <Platform> link should point to the correct URL

    Examples:
      | Platform |
      | Twitter  |
      | GitHub   |
      | LinkedIn |

  @responsive
  Scenario: TC-016 - Mobile layout hides sidebar and shows content
    Given the user navigates to the home page in mobile view
    Then the sidebar should be hidden
    And the hero tagline should be visible
    And the "About Me" heading should be visible

  @seo @sanity
  Scenario: TC-017 - Page meta tags are present
    Then the meta tag "description" should be present
    And the meta tag "viewport" should be present
    And the og meta tag "og:title" should be present

  @contact @validation
  Scenario: TC-018 - Email field rejects invalid format
    When the user navigates to the contact section
    And the user fills in the "Full Name" field with "Jane Doe"
    And the user fills in the "Email Address" field with "not-an-email"
    And the user fills in the "Subject" field with "Test"
    And the user fills in the "Message" field with "Testing email validation"
    And the user clicks the Send Message button
    Then the email field should show a format validation error

  @portfolio
  Scenario: TC-019 - Portfolio items have thumbnail images
    When the user clicks on the "Portfolio" link
    Then each portfolio item should have a visible image

  @navigation @ui
  Scenario: TC-020 - Navigation scrolls section into viewport
    When the user clicks on the "About Me" link
    Then the "About Me" heading should be in the viewport

  @links
  Scenario: TC-021 - Email mailto link is present in sidebar
    Then the Email link should be visible
    And the Email link should be a mailto link

  @ui
  Scenario: TC-022 - Resume PDF iframe has valid source
    When the user clicks on the "Resume" link
    Then the resume iframe should point to a PDF file
