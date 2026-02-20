#!/bin/bash
# run_tests.sh — Run Behave tests, collect results, and generate Allure report
#
# Usage:
#   ./run_tests.sh                     # full regression (all features)
#   ./run_tests.sh smoke               # smoke suite only
#   ./run_tests.sh sanity              # sanity suite only
#   ./run_tests.sh a11y                # accessibility suite
#   ./run_tests.sh perf                # performance suite
#   ./run_tests.sh --tags=@contact     # custom tag filter
#   ./run_tests.sh --name="TC-009"     # specific test by name

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

RESULTS_DIR="$SCRIPT_DIR/reports/allure-results"
REPORT_DIR="$SCRIPT_DIR/reports/allure-report"
HISTORY_DIR="$SCRIPT_DIR/reports/allure-history"

# Map suite shortcuts to behave arguments
BEHAVE_ARGS=""
TAGS_FILTER=""
SUITE_NAME="regression"

case "${1:-}" in
    smoke)
        BEHAVE_ARGS="--tags=@smoke"
        TAGS_FILTER="@smoke"
        SUITE_NAME="smoke"
        shift
        ;;
    sanity)
        BEHAVE_ARGS="--tags=@sanity"
        TAGS_FILTER="@sanity"
        SUITE_NAME="sanity"
        shift
        ;;
    a11y|accessibility)
        BEHAVE_ARGS="features/accessibility.feature"
        TAGS_FILTER="@a11y"
        SUITE_NAME="accessibility"
        shift
        ;;
    perf|performance)
        BEHAVE_ARGS="features/performance.feature"
        TAGS_FILTER="@performance"
        SUITE_NAME="performance"
        shift
        ;;
    *)
        # Pass through raw args (e.g., --tags=@contact or --name="TC-009")
        for arg in "$@"; do
            if [[ "$arg" == --tags=* ]]; then
                TAGS_FILTER="${arg#--tags=}"
            fi
        done
        BEHAVE_ARGS="$@"
        ;;
esac

# Preserve previous run's history for trend tracking
if [ -d "$REPORT_DIR/history" ]; then
    mkdir -p "$HISTORY_DIR"
    cp -R "$REPORT_DIR/history/"* "$HISTORY_DIR/" 2>/dev/null || true
fi

# Clean previous results (but not history)
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

# Copy history into results so Allure picks it up
if [ -d "$HISTORY_DIR" ]; then
    mkdir -p "$RESULTS_DIR/history"
    cp -R "$HISTORY_DIR/"* "$RESULTS_DIR/history/" 2>/dev/null || true
fi

# Run Behave
echo "🧪 Running $SUITE_NAME suite..."
python -m behave --no-capture $BEHAVE_ARGS || true

# Collect results into run history for the dashboard
echo ""
python "$SCRIPT_DIR/collect_results.py" "$TAGS_FILTER"

# Regenerate the test catalog from feature files
python "$SCRIPT_DIR/generate_catalog.py"

# Generate the Allure report
echo "📊 Generating Allure report..."
allure generate "$RESULTS_DIR" --clean -o "$REPORT_DIR"

echo ""
echo "✅ Done! ($SUITE_NAME)"
echo "   Dashboard:    open $SCRIPT_DIR/reports/dashboard.html"
echo "   Test Catalog: open $SCRIPT_DIR/reports/catalog.html"
echo "   Allure:       allure open $REPORT_DIR"
