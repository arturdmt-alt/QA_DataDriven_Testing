import pytest
import math
from typing import Any
from config.config_reader import config
from utils.logger import setup_logger

# Session-level logger
logger = setup_logger(__name__)


# =========================
# Utils
# =========================
def sanitize_value(value: Any) -> Any:
    """
    Sanitize test data values.

    Converts NaN values (from pandas) to empty strings
    to avoid invalid JSON payloads.
    """
    if isinstance(value, float) and math.isnan(value):
        return ""
    return value


# =========================
# Fixtures
# =========================
@pytest.fixture(scope="session")
def test_config():
    """
    Provide test configuration for the entire test session.
    """
    logger.info("Loading test configuration")
    return config


@pytest.fixture(scope="session")
def base_url(test_config):
    """
    Provide base URL for API testing.
    Fails early if base URL is not configured.
    """
    url = test_config.get_base_url()
    assert url, "Base URL is not configured"
    logger.info(f"Base URL configured: {url}")
    return url


@pytest.fixture(scope="function")
def test_logger(request):
    """
    Provide a dedicated logger per test to avoid duplicated handlers.
    """
    return setup_logger(request.node.name)


@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """
    Setup and teardown executed once per test session.
    """
    logger.info("=" * 80)
    logger.info("TEST SESSION STARTED")
    logger.info("=" * 80)

    yield

    logger.info("=" * 80)
    logger.info("TEST SESSION FINISHED")
    logger.info("=" * 80)


@pytest.fixture(scope="function", autouse=True)
def test_setup_teardown(request):
    """
    Setup and teardown executed before and after each test.
    """
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")

    yield

    logger.info(f"Finished test: {test_name}")
