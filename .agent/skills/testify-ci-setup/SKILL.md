---
name: testify-ci-setup
description: Set up a comprehensive Python/Behave Automation CI pipeline, Reporting, and Dashboard for a new or existing project.
---

# Testify CI/CD Setup Skill

This skill allows you to instantly scaffold a robust CI/CD pipeline, an Allure reporting integration, and a custom data-driven analytical dashboard into any repository.

## Overview

The `testify-ci-setup` skill provides pre-configured templates that you must copy directly into the user's workspace. It includes:
1. **GitHub Actions Workflow** (`test-suite.yml` & `setup-testify/action.yml`): Preconfigured for concurrent test execution (smoke, sanity, regression, etc.), linting, and GitHub Pages deployment.
2. **Bash Orchestrator** (`run_tests.sh`): Executes Behave tests and sequences the reporting generation.
3. **Python Metrics Collectors** (`collect_results.py`, `generate_catalog.py`): Scrapes Allure step data, generates a catalog, and tracks run history in UTC.
4. **Dynamic Frontend Dashboards** (`reports/dashboard.html` & `reports/catalog.html`): High-end UI templates rendering Chart.js graphs tracking historical test reliability.

## Instructions

When the user asks you to set up the CI or dashboard for a project using this skill, you MUST follow these steps exactly:

### 1. Identify the Target Directory
Ensure you are in the root of the user's project repository before proceeding.

### 2. Copy the Templates
Recursively copy the contents of this skill's `templates/` directory into the user's project root:
```bash
cp -r /path/to/.agent/skills/testify-ci-setup/templates/* ./
```
*Note: Make sure absolute paths are used for copying based on where this skill is located.*

### 3. Initialize Required Packages
Ensure the project's Python environment (e.g. `requirements.txt` or `Pipfile`) includes:
- `behave`
- `allure-behave`

### 4. Configure Behave Hooks
The reporting scripts depend on Allure correctly capturing failures. Verify or create `features/environment.py` in the target project, ensuring it has an `after_step` hook that attaches screenshots on step failure:
```python
import allure
def _capture_failure_screenshot(context, step):
    if hasattr(context, "page") and context.page:
        screenshot_bytes = context.page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"failure_screenshot_{step.name}",
            attachment_type=allure.attachment_type.PNG
        )

def after_step(context, step):
    if step.status == "failed":
        _capture_failure_screenshot(context, step)
```

### 5. Inform the User of System Requirements
After copying the templates, you MUST read this list to the user so they can finalize the GitHub settings:
- **Email Notifications**: They must add `SMTP_USERNAME` and `SMTP_PASSWORD` to their repository secrets if they wish to receive failure alerts.
- **GitHub Pages**: They must configure the repository settings to deploy Pages via GitHub Actions (Settings -> Pages -> Build and deployment source -> GitHub Actions).
- **Branch Protection**: The pipeline is configured to trigger on `main`.

### 6. Validation
- Run a linter if applicable.
- Make an initial commit of the new files and push to test the pipeline (if authorized by the user).
