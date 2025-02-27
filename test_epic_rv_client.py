# test_epic_rv_client.py
import os
from dotenv import load_dotenv
from epic_rv_client import EpicRvClient

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")
EPIC_DOMAIN = os.getenv("EPIC_DOMAIN", "https://api.twenty20solutions.com")
TEST_ENDPOINT = "/organization/00000001a01d1c4c9395f80b"

def main():
    client = EpicRvClient(
        email=EMAIL,
        password=PASSWORD,
        totp_secret=TOTP_SECRET,
        base_url=EPIC_DOMAIN,
    )
    
    if client.authenticate():
        response = client.get(TEST_ENDPOINT)
        if response.ok:
            data = response.json()
            print("Organization Name:", data.get("name"))
        else:
            print("Request failed with status:", response.status_code)
    else:
        print("Authentication failed.")

if __name__ == '__main__':
    main()
