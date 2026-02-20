#!/usr/bin/env python3
"""Collects Behave test results and appends them to a run history JSON file."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path(__file__).parent / "reports"
HISTORY_FILE = REPORTS_DIR / "run_history.json"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"


def parse_allure_results(results_dir: Path) -> dict:
    """Parse Allure result JSON files to extract test run data."""
    passed = 0
    failed = 0
    broken = 0
    skipped = 0
    total_duration_ms = 0
    scenarios = []

    for result_file in results_dir.glob("*-result.json"):
        try:
            with open(result_file) as f:
                result = json.load(f)

            status = result.get("status", "unknown")
            name = result.get("name", "Unknown")
            duration = result.get("stop", 0) - result.get("start", 0)
            labels = {label["name"]: label["value"] for label in result.get("labels", [])}

            if status == "passed":
                passed += 1
            elif status == "failed":
                failed += 1
            elif status == "broken":
                broken += 1
            elif status == "skipped":
                skipped += 1

            total_duration_ms += duration
            scenarios.append({
                "name": name,
                "status": status,
                "duration_ms": duration,
                "tags": labels.get("tag", ""),
            })
        except (json.JSONDecodeError, KeyError):
            continue

    total = passed + failed + broken + skipped
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "broken": broken,
        "skipped": skipped,
        "pass_rate": round((passed / total * 100), 1) if total > 0 else 0,
        "duration_s": round(total_duration_ms / 1000, 1),
        "scenarios": scenarios,
    }


def collect_and_save(tags_filter: str = ""):
    """Collect results and append to run history."""
    if not ALLURE_RESULTS_DIR.exists():
        print("⚠️  No allure-results directory found. Run tests first.")
        sys.exit(1)

    # Parse results
    run_data = parse_allure_results(ALLURE_RESULTS_DIR)
    run_data["timestamp"] = datetime.now().isoformat()
    run_data["run_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_data["tags_filter"] = tags_filter

    # Load existing history
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []

    # Append new run
    history.append(run_data)

    # Save history JSON
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    # Inject data into dashboard HTML so it works via file:// protocol
    inject_into_dashboard(history)

    print(f"📝 Run #{len(history)} recorded: {run_data['passed']}/{run_data['total']} passed ({run_data['pass_rate']}%)")


def inject_into_dashboard(history: list):
    """Embed run data directly into dashboard.html for file:// access."""
    dashboard_path = REPORTS_DIR / "dashboard.html"
    if not dashboard_path.exists():
        return

    html = dashboard_path.read_text()
    # Compact JSON for embedding (strip scenario details to keep file small)
    slim_history = []
    for run in history:
        slim = {k: v for k, v in run.items() if k != "scenarios"}
        slim_history.append(slim)

    data_line = f"        window.__RUN_DATA__ = {json.dumps(slim_history)};"
    html = re.sub(
        r"        window\.__RUN_DATA__ = .*?;",
        data_line,
        html
    )
    dashboard_path.write_text(html)


if __name__ == "__main__":
    tags = sys.argv[1] if len(sys.argv) > 1 else ""
    collect_and_save(tags)
