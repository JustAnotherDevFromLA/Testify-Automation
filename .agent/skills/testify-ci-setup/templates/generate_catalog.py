#!/usr/bin/env python3
"""Parse all .feature files and generate a test catalog JSON + inject into catalog.html."""

import json
import re
from pathlib import Path

FEATURES_DIR = Path(__file__).parent / "features"
REPORTS_DIR = Path(__file__).parent / "reports"
CATALOG_FILE = REPORTS_DIR / "test_catalog.json"
CATALOG_HTML = REPORTS_DIR / "catalog.html"


def parse_feature_file(filepath: Path) -> dict:
    """Parse a .feature file and extract scenarios with tags."""
    lines = filepath.read_text().splitlines()

    feature_name = ""
    feature_tags = []
    scenarios = []
    current_tags = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Collect tags
        if line.startswith("@"):
            tags = re.findall(r"@\w+", line)
            # Check if next non-empty line is Feature or Scenario
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                if next_line.startswith("Feature:"):
                    feature_tags = tags
                else:
                    current_tags = tags
            i += 1
            continue

        # Feature line
        if line.startswith("Feature:"):
            feature_name = line.replace("Feature:", "").strip()
            i += 1
            continue

        # Scenario / Scenario Outline
        if line.startswith("Scenario:") or line.startswith("Scenario Outline:"):
            is_outline = line.startswith("Scenario Outline:")
            name = re.sub(r"^Scenario( Outline)?:\s*", "", line)

            # Extract TC-ID
            tc_match = re.match(r"(TC-[A-Z]?\d+)", name)
            tc_id = tc_match.group(1) if tc_match else ""
            description = re.sub(r"^TC-[A-Z]?\d+\s*-\s*", "", name).strip()

            # Collect steps
            steps = []
            j = i + 1
            examples = []
            in_examples = False
            while j < len(lines):
                step_line = lines[j].strip()
                if step_line == "" and not in_examples:
                    j += 1
                    continue
                if step_line.startswith("@") or step_line.startswith("Scenario"):
                    break
                if step_line.startswith("Examples:"):
                    in_examples = True
                    j += 1
                    continue
                if in_examples and step_line.startswith("|"):
                    examples.append(step_line)
                    j += 1
                    continue
                if in_examples and not step_line.startswith("|"):
                    break
                if step_line.startswith(("Given ", "When ", "Then ", "And ", "But ")) or step_line.startswith("|"):
                    steps.append(step_line)
                j += 1

            # Count example rows (minus header)
            example_count = max(0, len(examples) - 1) if examples else 0

            all_tags = list(set(feature_tags + current_tags))
            all_tags.sort()

            scenario = {
                "tc_id": tc_id,
                "name": description,
                "tags": all_tags,
                "steps": steps,
                "is_outline": is_outline,
                "example_count": example_count,
                "feature": feature_name,
                "file": filepath.name,
            }
            scenarios.append(scenario)
            current_tags = []
            i = j
            continue

        i += 1

    return {
        "feature": feature_name,
        "file": filepath.name,
        "tags": feature_tags,
        "scenarios": scenarios,
    }


def build_catalog():
    """Build catalog from all feature files."""
    features = []
    for f in sorted(FEATURES_DIR.glob("*.feature")):
        parsed = parse_feature_file(f)
        if parsed["scenarios"]:
            features.append(parsed)

    # Build summary
    all_scenarios = [s for f in features for s in f["scenarios"]]
    all_tags = set()
    for s in all_scenarios:
        all_tags.update(s["tags"])

    # Determine suite membership
    suite_map = {
        "smoke": [],
        "sanity": [],
        "regression": [],
        "accessibility": [],
        "performance": [],
    }
    for s in all_scenarios:
        tags = s["tags"]
        name = s["tc_id"]
        if "@smoke" in tags:
            suite_map["smoke"].append(name)
        if "@sanity" in tags:
            suite_map["sanity"].append(name)
        if "@regression" in tags:
            suite_map["regression"].append(name)
        if "@a11y" in tags or "@accessibility" in tags:
            suite_map["accessibility"].append(name)
        if "@perf" in tags or "@performance" in tags:
            suite_map["performance"].append(name)

    catalog = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "total_features": len(features),
        "total_scenarios": len(all_scenarios),
        "total_with_examples": sum(s["example_count"] if s["example_count"] > 0 else 1 for s in all_scenarios),
        "all_tags": sorted(all_tags),
        "suites": {k: {"count": len(v), "tests": v} for k, v in suite_map.items()},
        "features": features,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_FILE, "w") as f:
        json.dump(catalog, f, indent=2)

    # Inject into catalog.html
    inject_into_html(catalog)

    print(f"📋 Test catalog generated: {len(all_scenarios)} test cases across {len(features)} features")
    for suite, data in catalog["suites"].items():
        if data["count"] > 0:
            print(f"   {suite}: {data['count']} tests")


def inject_into_html(catalog: dict):
    """Inject catalog data into catalog.html."""
    if not CATALOG_HTML.exists():
        return
    html = CATALOG_HTML.read_text()
    data_line = f"        window.__CATALOG__ = {json.dumps(catalog)};"
    html = re.sub(
        r"        window\.__CATALOG__ = .*?;",
        data_line,
        html,
    )
    CATALOG_HTML.write_text(html)


if __name__ == "__main__":
    build_catalog()
