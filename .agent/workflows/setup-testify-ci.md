---
description: Set up the Testify Automation CI/CD Pipeline and Dashboard
---

# Testify CI/CD & Dashboard Setup Workflow

This workflow is meant to be run when setting up a new automation project that requires the robust CI/CD, Allure reporting, custom Quality Dashboard, and Email Notifications built for the Testify architecture.

## Overview of Components

To replicate this setup on a new project, you need to copy over the following core components:

### 1. GitHub Actions Pipelines
- **Test Suite Workflow (`.github/workflows/test-suite.yml`)**: Contains all the concurrent jobs (`quality`, `smoke`, `sanity`, `regression`, `accessibility`, `performance`), merging logic, and GitHub pages deployment.
- **Custom Setup Action (`.github/actions/setup-testify/action.yml`)**: A composite action to DRY up Python and dependencies installation for every job.

### 2. Reporting Scripts
These Python scripts parse the Allure step execution output and compile it into historical data sets.
- **`collect_results.py`**: Parses Allure's JSON results to track `passed`, `failed`, `skipped` test cases. Injects historical test data securely wrapped in explicit UTC constraints into `run_history.json`.
- **`generate_catalog.py`**: Reads `.feature` files and syncs scenario contexts into static dictionaries.

### 3. Dashboard Templates
- **`reports/dashboard.html`**: A static glassmorphism frontend that renders trend graphs using Chart.js.
- **`reports/catalog.html`**: The test case catalog view.

### 4. Runner & Environment
- **`run_tests.sh`**: The cross-platform orchestrator script that invokes behaviors and reporting consecutively.
- **`features/environment.py`**: Behave lifecycle hooks. Must contain Allure screenshot attachment injection inside `_capture_failure_screenshot`.

## Automated Implementation Steps

When instructed by the user to use this workflow for a new project, follow these exact steps:

1. Initialization
   ```bash
   mkdir -p .github/workflows .github/actions/setup reports
   ```

2. Port over the core testing bash runner and Python reporting utilities (`run_tests.sh`, `collect_results.py`, `generate_catalog.py`).

3. Port over the front-end components: copy all HTML UI from the `reports/` directory into the new project's directory. 

4. Configure Behave & Allure
   - Ensure the new project has `allure-behave` installed and hooked in `features/environment.py`. 
   - Check that `allure.attach()` logic is present on test failures to support screenshot artifacts.

5. Update Workflow Secrets
   - Inform the user they must add `SMTP_USERNAME` and `SMTP_PASSWORD` to the new GitHub repository's secrets if they want the failure-notification emails to work.
   - Inform the user to configure the repo to allow GitHub Pages deployment from GitHub Actions (under Repository Settings -> Pages -> Build and deployment source). 

6. Port over `.github/workflows/test-suite.yml`
   - Adjust matrix logic or parallel suites if the newly targeted project has a different tagging architecture than `@smoke`, `@sanity`, `@regression`.

7. Commit and Validate
   - Execute a lint pass using `ruff`.
   - Push to main and verify GitHub Pages successfully serves the `.html` dashboard out of the `reports` folder artifact.
