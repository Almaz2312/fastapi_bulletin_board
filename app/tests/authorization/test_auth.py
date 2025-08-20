import pytest

pytest_plugins = ["pytest_asyncio"]
pytestmark = pytest.mark.asyncio


class TestAuth:
    base_url = "/api/v1/auth/login"
