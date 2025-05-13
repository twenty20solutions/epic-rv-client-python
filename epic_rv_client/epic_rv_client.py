import requests
import pyotp


class EpicRvClient:
    """
    A Python client for authenticating and making requests to the EpicRv API.

    Args:
        email (str): The email (username).
        password (str): The password.
        totp_secret (str, optional): The TOTP secret for 2FA.
        base_url (str, optional): Base URL for the API (default: https://api.twenty20solutions.com).
    """

    def __init__(self, email, password, totp_secret=None, base_url='https://api.twenty20solutions.com'):
        if not email or not password:
            raise ValueError("email and password are required")
        self.email = email
        self.password = password
        self.totp_secret = totp_secret
        self.base_url = base_url
        self.session = requests.Session()  # Session automatically handles cookies

    def authenticate(self):
        """Perform login and, if needed, complete two-factor authentication."""
        # 1) Basic login (POST /auth/login)
        login_payload = {
            "email": self.email,
            "password": self.password
        }
        login_url = f"{self.base_url}/auth/login"
        login_res = self.session.post(login_url, json=login_payload)
        if not login_res.ok:
            msg = self._extract_error_message(login_res)
            raise Exception(f"Login failed. HTTP {login_res.status_code}: {msg}")

        login_data = login_res.json()
        # 2) Check if two-factor authentication is required
        needs_2fa = login_data and login_data.get("code") == 1003
        if needs_2fa:
            if not self.totp_secret:
                raise Exception("2FA required but totp_secret was not provided!")
            code = self._generate_totp()
            second_factor_url = f"{self.base_url}/auth/secondFactor"
            second_factor_res = self.session.post(second_factor_url, json={"key": code})
            if not second_factor_res.ok:
                msg = self._extract_error_message(second_factor_res)
                raise Exception(f"2FA failed. HTTP {second_factor_res.status_code}: {msg}")
        return True

    def _generate_totp(self):
        """Generate a TOTP code using pyotp."""
        return pyotp.TOTP(self.totp_secret).now()

    def _extract_error_message(self, response):
        """Extract error message from a response."""
        try:
            return response.text or response.reason
        except Exception as err:
            return str(err)

    def request(self, method, url, body=None, **options):
        """
        Generic request wrapper supporting all HTTP methods.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.).
            url (str): Relative or absolute URL.
            body (dict or str, optional): JSON body or string/bytes for request.
            **options: Additional options passed to requests.request.

        Returns:
            Response: The response object from requests.
        """
        headers = options.pop("headers", {})
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"

        # If body is a dict, assume JSON
        if body is not None and isinstance(body, dict):
            headers.setdefault("Content-Type", "application/json")
            response = self.session.request(method.upper(), full_url, headers=headers, json=body, **options)
        else:
            response = self.session.request(method.upper(), full_url, headers=headers, data=body, **options)
        return response

    # Convenience wrappers
    def get(self, url, **options):
        return self.request("GET", url, None, **options)

    def post(self, url, body, **options):
        return self.request("POST", url, body, **options)

    def put(self, url, body, **options):
        return self.request("PUT", url, body, **options)

    def patch(self, url, body, **options):
        return self.request("PATCH", url, body, **options)

    def delete(self, url, **options):
        return self.request("DELETE", url, None, **options)

    def head(self, url, **options):
        return self.request("HEAD", url, None, **options)

    def options(self, url, **options):
        return self.request("OPTIONS", url, None, **options)

    def update_equipment(self, equipment_id, external_ip=None, http_port=None, rtsp_port=None):
        settings = {}
        if external_ip:
            settings["externalIp"] = external_ip
        if http_port:
            settings["httpAlt"] = int(http_port)
            settings["externalPort"] = int(http_port)
        if rtsp_port:
            settings["rtspPort"] = int(rtsp_port)

        if not settings:
            return None

        payload = {"settings": settings}
        return self.put(f"/equipment/{equipment_id}", body=payload)

    def update_rcu(self, rcu_id, external_ip=None, http_port=None):
        # Fetch current RCU object to check kind
        response = self.get(f"/rcu/{rcu_id}")
        if not response.ok:
            print(f"❌ Failed to fetch RCU {rcu_id}: {response.status_code}")
            return response

        rcu_data = response.json()
        if rcu_data.get("kind", "PHYSICAL").upper() == "VIRTUAL":
            print(f"⚠️  Skipping RCU {rcu_id} — it's a VIRTUAL RCU")
            return None

        payload = {}
        if external_ip:
            payload["ip"] = external_ip
        if http_port:
            payload["port"] = int(http_port)

        if not payload:
            print(f"⚠️  Nothing to update for RCU {rcu_id}")
            return None

        return self.put(f"/rcu/{rcu_id}", body=payload)
