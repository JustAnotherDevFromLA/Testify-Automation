# Testify Automation

Automated test suite for [artasheskocharyan.com](https://artasheskocharyan.com) — a personal portfolio site built as a single-page application. Tests are written in **Gherkin** (BDD) using **Behave** and **Playwright** (Chromium, headless).

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Test Suites](#test-suites)
- [Project Structure](#project-structure)
- [Reporting](#reporting)
- [CI/CD](#cicd)
- [Writing New Tests](#writing-new-tests)
- [Troubleshooting](#troubleshooting)

---

## Features

| Capability | Details |
|---|---|
| **26 test cases** across 3 feature files | Regression, accessibility, performance |
| **Tag-based filtering** | Run smoke, sanity, or specific category tests |
| **Page Object Model** | Selectors isolated in reusable page classes |
| **Allure reporting** | Rich per-scenario results with failure screenshots |
| **Run tracking dashboard** | Pass rate trends, duration tracking, run history |
| **Auto-generated test catalog** | Browsable view of all test cases by suite and tag |
| **CI/CD pipeline** | GitHub Actions with smoke → sanity → regression stages |
| **Network resilience** | Auto-retry on transient connection errors |

---

## Prerequisites

- **Python 3.10+**
- **Allure CLI** (for report generation)
  ```bash
  brew install allure   # macOS
  ```

---

## Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Automation

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
python -m playwright install chromium
```

---

## Running Tests

All tests are run through `run_tests.sh`, which handles execution, result collection, catalog generation, and Allure report creation in one command.

### Quick Start

```bash
# Run the full regression suite (all 36 scenarios)
./run_tests.sh

# Open the dashboard
open reports/dashboard.html

# Open the Allure report
allure open reports/allure-report
```

### Suite Shortcuts

| Command | Suite | Scenarios | Typical Duration |
|---|---|---|---|
| `./run_tests.sh` | Full regression | 36 | ~30s |
| `./run_tests.sh smoke` | Smoke (critical path) | 3 | ~3s |
| `./run_tests.sh sanity` | Sanity (happy path) | ~14 | ~10s |
| `./run_tests.sh a11y` | Accessibility | 5 | ~3s |
| `./run_tests.sh perf` | Performance | 3 | ~3s |

### Tag Filtering

```bash
# Run all contact form tests
./run_tests.sh --tags=@contact

# Run all portfolio tests
./run_tests.sh --tags=@portfolio

# Run a specific test by name
./run_tests.sh --name="TC-009"

# Run directly with Behave (no report generation)
python -m behave --no-capture --tags=@smoke
```

---

## Test Suites

### Regression (`@regression`) — 18 test cases

The core test suite covering all sections of the site.

| ID | Scenario | Tags |
|---|---|---|
| TC-001 | Page title verification | `@smoke` `@sanity` |
| TC-002 | Navigation to each section (×4) | `@navigation` `@sanity` |
| TC-003 | Social links visible (×3) | `@links` `@sanity` |
| TC-004 | PDF viewer in Resume section | `@ui` `@sanity` |
| TC-005 | Hero CTA scrolls to Portfolio | `@ui` `@smoke` `@sanity` |
| TC-006 | Contact form fields present | `@contact` `@smoke` `@sanity` |
| TC-007 | Fill out contact form | `@contact` |
| TC-008 | Required field validation | `@contact` `@validation` |
| TC-009 | Hero section content displayed | `@ui` `@sanity` |
| TC-010 | About Me key content | `@content` |
| TC-011 | All portfolio items displayed | `@portfolio` |
| TC-012 | Portfolio items link to GitHub (×4) | `@portfolio` |
| TC-013 | Resume download link | `@ui` |
| TC-014 | Footer copyright | `@ui` `@sanity` |
| TC-015 | Social links correct URLs (×3) | `@links` |
| TC-016 | Mobile layout hides sidebar | `@responsive` |
| TC-017 | Meta tags present | `@seo` `@sanity` |
| TC-018 | Email format validation | `@contact` `@validation` |

### Accessibility (`@accessibility`) — 5 test cases

| ID | Scenario |
|---|---|
| TC-A01 | All images have alt text |
| TC-A02 | Heading hierarchy is correct |
| TC-A03 | Page has a lang attribute |
| TC-A04 | Interactive elements are keyboard accessible |
| TC-A05 | Body text meets minimum font size |

### Performance (`@performance`) — 3 test cases

| ID | Scenario |
|---|---|
| TC-P01 | Page loads within 5 seconds |
| TC-P02 | No broken images |
| TC-P03 | DOM element count under 1500 |

---

## Project Structure

```
Automation/
├── .github/workflows/
│   └── test-suite.yml          # CI/CD pipeline config
├── features/
│   ├── regression.feature      # 18 regression test cases
│   ├── accessibility.feature   # 5 a11y test cases
│   ├── performance.feature     # 3 performance test cases
│   ├── environment.py          # Behave hooks (browser setup/teardown)
│   └── steps/
│       ├── home_steps.py       # Navigation, content, UI steps
│       ├── contact_steps.py    # Contact form steps
│       ├── portfolio_steps.py  # Portfolio item steps
│       ├── responsive_steps.py # Mobile viewport steps
│       ├── accessibility_steps.py
│       └── performance_steps.py
├── pages/                      # Page Object Model
│   ├── base_page.py            # Base class with retry logic
│   ├── home_page.py            # Main page selectors & actions
│   ├── contact_page.py         # Contact form selectors & actions
│   └── responsive_page.py     # Mobile viewport testing
├── reports/                    # Generated reports (gitignored except templates)
│   ├── dashboard.html          # Run tracking dashboard
│   └── catalog.html            # Auto-generated test catalog
├── run_tests.sh                # One-command test runner
├── collect_results.py          # Allure result parser → dashboard
├── generate_catalog.py         # Feature file parser → catalog
├── behave.ini                  # Behave configuration
├── requirements.txt            # Python dependencies
└── TEST_STRATEGY.md            # Full test strategy document
```

---

## Reporting

Every `./run_tests.sh` execution automatically produces three reports:

### 1. Dashboard (`reports/dashboard.html`)

A standalone HTML page with:
- Pass rate trend chart over time
- Duration tracking per run
- Run history table with status, pass rate, and tag filter
- Links to the test catalog

```bash
open reports/dashboard.html
```

### 2. Test Catalog (`reports/catalog.html`)

An auto-generated, searchable view of all test cases:
- Filter by suite (smoke, sanity, regression, a11y, performance)
- Search by test ID, name, or tag
- Expand any test to see its Gherkin steps
- Regenerated from `.feature` files on every run

```bash
open reports/catalog.html
```

### 3. Allure Report

Rich interactive report with per-scenario details, step breakdowns, and failure screenshots:

```bash
allure open reports/allure-report
```

---

## CI/CD

The project includes a GitHub Actions pipeline (`.github/workflows/test-suite.yml`) with four stages:

| Stage | Trigger | Suite | On Failure |
|---|---|---|---|
| **Pre-merge** | Every PR | `@smoke` | Blocks merge |
| **Post-merge** | Push to `main` | `@sanity` | Alerts team |
| **Nightly** | Cron (2 AM UTC) | Full regression + Allure | Creates issue |
| **Manual** | `workflow_dispatch` | Any suite (selectable) | — |

### Manual Dispatch

You can trigger any suite manually from the GitHub Actions tab by selecting the `workflow_dispatch` trigger and choosing a suite.

---

## Writing New Tests

### 1. Add a Scenario

Add your scenario to the appropriate `.feature` file with a unique TC-ID and relevant tags:

```gherkin
@portfolio
Scenario: TC-019 - Portfolio loads project images
  When the user clicks on the "Portfolio" link
  Then each portfolio item should have an image
```

### 2. Add Page Object Methods (if needed)

If your test interacts with new elements, add selectors and methods to the appropriate page object in `pages/`:

```python
# pages/home_page.py
PORTFOLIO_IMAGE = '.portfolio-item img'

def verify_portfolio_images(self):
    images = self.page.locator(self.PORTFOLIO_IMAGE)
    expect(images.first).to_be_visible()
```

### 3. Add Step Definitions

Create the corresponding step in `features/steps/`:

```python
@then('each portfolio item should have an image')
def step_verify_portfolio_images(context):
    context.home_page.verify_portfolio_images()
```

### 4. Run and Verify

```bash
# Run just your new test
./run_tests.sh --name="TC-019"

# Run the full suite to check for regressions
./run_tests.sh
```

The test catalog will auto-update to include your new scenario.

---

## Troubleshooting

### Tests fail with `net::ERR_INTERNET_DISCONNECTED`

This is a transient network error. The base page object retries navigation up to 3 times with a 2-second backoff. If it persists:
- Check your internet connection
- Try running a smaller suite first: `./run_tests.sh smoke`
- Increase retries in `pages/base_page.py` if needed

### `allure: command not found`

Install the Allure CLI:
```bash
brew install allure          # macOS
sudo apt install allure      # Debian/Ubuntu
```

Or skip Allure and run tests directly:
```bash
python -m behave --no-capture
```

### Browser not installed

```bash
python -m playwright install chromium
```

### Tests pass individually but fail in the full suite

Typically caused by network instability under rapid sequential requests. The retry logic handles most cases. If issues persist, try adding a brief delay between feature files or running suites independently.

---

## License

This project is for personal/educational use.
