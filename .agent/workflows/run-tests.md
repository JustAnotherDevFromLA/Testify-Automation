---
description: How to run the test suite and update the dashboard
---

# Running the Test Suite

Always use `./run_tests.sh` to run tests — this ensures the dashboard, test catalog, and Allure report are all updated.

// turbo-all

## Steps

1. Activate the virtual environment and run the test suite:
```bash
source venv/bin/activate && ./run_tests.sh
```

2. To run a specific suite:
```bash
source venv/bin/activate && ./run_tests.sh smoke    # or: sanity, a11y, perf
```

3. To run with tag filtering:
```bash
source venv/bin/activate && ./run_tests.sh --tags=@contact
```

4. To run a specific test by name:
```bash
source venv/bin/activate && ./run_tests.sh --name="TC-009"
```

## Important

- **Never** use `python -m behave` directly — it skips result collection and the dashboard won't update.
- `./run_tests.sh` handles: test execution → result collection → catalog generation → Allure report.
