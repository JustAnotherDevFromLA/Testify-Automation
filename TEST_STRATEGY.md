# Test Strategy — artasheskocharyan.com

## 1. Objective

Ensure the quality, reliability, and user experience of artasheskocharyan.com through structured automated test suites organized by purpose and risk level.

---

## 2. Application Under Test

| Attribute | Value |
|---|---|
| **URL** | https://artasheskocharyan.com |
| **Type** | Personal portfolio — single-page application |
| **Sections** | Intro (Hero), About Me, Portfolio, Resume, Contact |
| **Key Features** | Navigation sidebar, social links, portfolio gallery, embedded PDF resume, contact form with validation |
| **Responsive** | Desktop sidebar layout → mobile single-column |

---

## 3. Test Suite Definitions

### 3.1 Smoke Suite (`@smoke`)

> **Purpose**: Verify the application is accessible and core functionality is not broken. Run on every deploy and before any deeper testing.
>
> **Execution time target**: < 5 seconds
>
> **When to run**: Every deployment, every PR merge, CI/CD pipeline trigger

| TC ID | Scenario | Rationale |
|---|---|---|
| TC-001 | Page title is correct | Confirms the app loads without a server error |
| TC-005 | Hero CTA scrolls to Portfolio | Confirms JS is functional and page structure intact |
| TC-006 | Contact form fields are present | Confirms the most critical interactive section renders |

**Tag**: `@smoke`
**Run command**: `./run_tests.sh --tags=@smoke`

---

### 3.2 Sanity Suite (`@sanity`)

> **Purpose**: Validate that all major sections and features work correctly after a change. Broader than smoke but focused on happy-path functionality — no edge cases.
>
> **Execution time target**: < 15 seconds
>
> **When to run**: After content updates, CSS/layout changes, or dependency upgrades

| TC ID | Scenario | Rationale |
|---|---|---|
| TC-001 | Page title is correct | Basic load verification |
| TC-002 ×4 | Navigation to each section works | All section links functional |
| TC-003 ×3 | Social links (Twitter, GitHub, LinkedIn) visible | External links render |
| TC-004 | PDF viewer in Resume section | Embedded content loads |
| TC-005 | Hero CTA scrolls to Portfolio | JS interaction works |
| TC-006 | Contact form fields present | Form renders correctly |
| TC-009 | Hero section content displayed | Profile image, name, tagline |
| TC-014 | Footer displays copyright | Page structure complete |
| TC-017 | Meta tags present | SEO fundamentals intact |

**Tag**: `@sanity`
**Run command**: `./run_tests.sh --tags=@sanity`

---

### 3.3 Regression Suite (`@regression`)

> **Purpose**: Full end-to-end validation of every feature, including edge cases, validation rules, and responsive behavior. Catches regressions introduced by any change.
>
> **Execution time target**: < 30 seconds
>
> **When to run**: Before releases, weekly scheduled runs, after major refactors

| TC ID | Tag | Scenario | Category |
|---|---|---|---|
| TC-001 | `@smoke` | Page title verification | Core |
| TC-002 ×4 | `@navigation` | Navigation to each section | Navigation |
| TC-003 ×3 | `@links` | Social links visible | Links |
| TC-004 | `@ui` | PDF viewer in Resume | Content |
| TC-005 | `@ui` | Hero CTA scrolls to Portfolio | UI |
| TC-006 | `@contact` | Contact form fields present | Forms |
| TC-007 | `@contact` | Fill out contact form | Forms |
| TC-008 | `@contact @validation` | Required field validation | Validation |
| TC-009 | `@ui` | Hero content (image, name, tagline) | UI |
| TC-010 | `@content` | About Me key content | Content |
| TC-011 | `@portfolio` | All 6 portfolio items displayed | Portfolio |
| TC-012 ×4 | `@portfolio` | Portfolio items link to GitHub | Portfolio |
| TC-013 | `@ui` | Resume download link | Content |
| TC-014 | `@ui` | Footer copyright | UI |
| TC-015 ×3 | `@links` | Social links point to correct URLs | Links |
| TC-016 | `@responsive` | Mobile layout hides sidebar | Responsive |
| TC-017 | `@seo` | Meta tags present | SEO |
| TC-018 | `@contact @validation` | Email format validation | Validation |

**Total**: 28 scenarios across 18 test cases
**Tag**: `@regression`
**Run command**: `./run_tests.sh` (runs everything by default)

---

## 4. Tag Architecture

Tags allow selective execution. Each scenario has a **category tag** and may be part of multiple suites.

```
@regression          ← every scenario (top-level feature tag)
├── @smoke           ← critical path (TC-001, TC-005, TC-006)
├── @sanity          ← happy-path validation (smoke + core sections)
├── @navigation      ← section link tests
├── @links           ← social link visibility & URL checks
├── @ui              ← visual element presence
├── @content         ← text content verification
├── @portfolio       ← portfolio items & links
├── @contact         ← contact form tests
├── @validation      ← form validation edge cases
├── @responsive      ← mobile viewport tests
└── @seo             ← meta tags & SEO checks
```

### Run by category:
```bash
./run_tests.sh --tags=@smoke          # 3 scenarios, ~3s
./run_tests.sh --tags=@sanity         # ~14 scenarios, ~10s
./run_tests.sh --tags=@contact        # 4 scenarios
./run_tests.sh --tags=@portfolio      # 5 scenarios
./run_tests.sh --tags=@links          # 6 scenarios
./run_tests.sh --tags=@responsive     # 1 scenario
```

---

## 5. Test Pyramid & Coverage Map

```
             ┌─────────────────┐
             │   Responsive    │  ← TC-016 (mobile viewport)
             │   & SEO         │  ← TC-017 (meta tags)
             ├─────────────────┤
             │   Validation    │  ← TC-008, TC-018 (form edge cases)
             │   Edge Cases    │
         ┌───┴─────────────────┴───┐
         │   Functional Tests      │  ← TC-002–TC-015
         │   (Navigation, Content, │    (links, portfolio, resume,
         │    Forms, Portfolio)     │     contact form, footer)
     ┌───┴─────────────────────────┴───┐
     │       Smoke / Core              │  ← TC-001, TC-005, TC-006
     │       (Page loads, JS works)    │    (title, CTA, form render)
     └─────────────────────────────────┘
```

### Section Coverage Matrix

| Section | UI | Content | Links | Forms | Responsive | SEO |
|---|---|---|---|---|---|---|
| **Hero/Intro** | TC-005, TC-009 | — | — | — | TC-016 | — |
| **About Me** | TC-002 | TC-010 | — | — | TC-016 | — |
| **Portfolio** | TC-002, TC-011 | — | TC-012 ×4 | — | — | — |
| **Resume** | TC-004, TC-013 | — | — | — | — | — |
| **Contact** | TC-006 | — | — | TC-007, TC-008, TC-018 | — | — |
| **Sidebar/Nav** | TC-009 | — | TC-003, TC-015 | — | TC-016 | — |
| **Footer** | TC-014 | — | — | — | — | — |
| **Page-level** | TC-001 | — | — | — | — | TC-017 |

---

## 6. Execution Strategy

### CI/CD Pipeline

| Stage | Suite | Trigger | Failure Action |
|---|---|---|---|
| **Pre-merge** | `@smoke` | Every PR | Block merge |
| **Post-merge** | `@sanity` | Main branch push | Alert team |
| **Nightly** | `@regression` | Scheduled (cron) | Create issue |
| **Pre-release** | `@regression` | Manual trigger | Block release |

### Local Development

```bash
# Quick check after changes
./run_tests.sh --tags=@smoke

# Validate a specific area
./run_tests.sh --tags=@contact

# Full suite before pushing
./run_tests.sh
```

---

## 7. Reporting & Tracking

| Tool | Purpose | Access |
|---|---|---|
| **Dashboard** | Run history, trends, pass rates | `open reports/dashboard.html` |
| **Allure Report** | Detailed per-scenario results, screenshots on failure | `allure open reports/allure-report` |
| **Run History** | JSON log of all runs | `reports/run_history.json` |

Every `./run_tests.sh` execution automatically:
1. Runs the test suite
2. Records results in `run_history.json`
3. Updates the dashboard
4. Generates an Allure report

---

## 8. Environment & Configuration

| Component | Value |
|---|---|
| **Framework** | Behave (Python BDD) |
| **Browser Engine** | Playwright + Chromium |
| **Mode** | Headless (`headless=True` in `environment.py`) |
| **Viewport** | Desktop: 1280×720, Mobile: 375×667 |
| **Allure** | allure-behave for result collection |
| **Config** | `behave.ini` |

---

## 9. Risk Matrix

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| Site goes offline | All tests fail | Low | Retry logic; smoke test distinguishes server errors from bugs |
| Network instability | Intermittent failures | Medium | `net::ERR_INTERNET_DISCONNECTED` errors flagged on dashboard |
| CSS selector changes | Tests break silently | Medium | Page Object Model isolates selectors; single point of change |
| Third-party link changes | TC-012, TC-015 fail | Low | URL fragments tested, not full URLs |
| Mobile layout refactor | TC-016 fails | Low | Bounding-rect check is resilient to CSS approach changes |

---

## 10. Future Enhancements

| Enhancement | Priority | Description |
|---|---|---|
| **Performance tests** | Medium | Assert page load < 3s, LCP < 2.5s |
| **Accessibility (a11y)** | High | ARIA labels, alt text, keyboard nav, color contrast |
| **Visual regression** | Medium | Pixel-diff screenshots with Playwright `toHaveScreenshot()` |
| **Cross-browser** | Low | Run on Firefox, WebKit in addition to Chromium |
| **API monitoring** | Low | Health check endpoint, uptime tracking |
| **Login/Signup flows** | Medium | Tests for `/login` and `/signup` pages |
