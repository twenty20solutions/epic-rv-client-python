import os
import pytest
from dotenv import load_dotenv
from epic_rv_client import EpicRvClient

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")
EPIC_DOMAIN = os.getenv("EPIC_DOMAIN", "https://api.twenty20solutions.com")
TEST_ENDPOINT = "/organization/00000001a01d1c4c9395f80b"

@pytest.mark.integration
def test_auth_and_get_organization():
    if not all([EMAIL, PASSWORD, TOTP_SECRET]):
        pytest.skip("Missing credentials in environment variables")

    client = EpicRvClient(
        email=EMAIL,
        password=PASSWORD,
        totp_secret=TOTP_SECRET,
        base_url=EPIC_DOMAIN,
    )

    assert client.authenticate(), "Authentication failed"

    response = client.get(TEST_ENDPOINT)
    assert response.ok, f"GET request failed: {response.status_code} - {response.text}"

    data = response.json()
    assert "name" in data, "Response missing 'name' field"
