"""
Centralized configuration for the Testify Automation test suite.

All settings can be overridden via environment variables, allowing the same
suite to run against different environments (dev, staging, production) without
code changes.

Usage:
    import config
    config.BASE_URL  # defaults to production, override with BASE_URL env var
"""

import os

# ── Target ──────────────────────────────────────────────────────────────────
BASE_URL: str = os.getenv("BASE_URL", "https://artasheskocharyan.com")

# ── Browser ─────────────────────────────────────────────────────────────────
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER: str = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1280"))
VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "720"))

# ── Timeouts & Retries ─────────────────────────────────────────────────────
DEFAULT_TIMEOUT_MS: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
NAVIGATION_TIMEOUT_MS: int = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))
RETRY_ATTEMPTS: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
RETRY_DELAY_S: int = int(os.getenv("RETRY_DELAY", "2"))

# ── Logging ─────────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
