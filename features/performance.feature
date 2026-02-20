@performance
Feature: Performance Suite for artasheskocharyan.com

  @perf
  Scenario: TC-P01 - Page loads within acceptable time
    When the user measures the page load time
    Then the page should load in less than 5 seconds

  @perf
  Scenario: TC-P02 - No broken images on the page
    Given the user navigates to the home page
    Then all images should load successfully

  @perf
  Scenario: TC-P03 - Page size is reasonable
    Given the user navigates to the home page
    Then the total DOM element count should be less than 1500
