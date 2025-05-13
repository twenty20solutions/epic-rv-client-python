# epic_rv_client

A lightweight Python client for authenticating and making API requests to the [EPIC RV](https://remotevision.epicio.com) platform. Supports 2FA using TOTP.

![Tests](https://github.com/twenty20solutions/epic-rv-client-python/actions/workflows/python-tests.yml/badge.svg)

---

## 📦 Installation

### With pipenv

```bash
pipenv install "git+https://github.com/twenty20solutions/epic-rv-client-python.git#egg=epic_rv_client"
```

### Or with pip

```bash
pip install "git+https://github.com/twenty20solutions/epic-rv-client-python.git"
```

---

## 🧰 Features

- Secure authentication with `email`/`password`
- Optional support for TOTP-based 2FA
- Session-based request handling (cookies maintained)
- Helper methods for all major HTTP verbs: `GET`, `POST`, `PUT`, `DELETE`, etc.

---

## 🚀 Usage

```python
from epic_rv_client import EpicRvClient

client = EpicRvClient(
    email="your@email.com",
    password="yourpassword",
    totp_secret="YOUR_TOTP_SECRET",  # Optional if 2FA not enabled
    base_url="https://api.twenty20solutions.com"
)

client.authenticate()

response = client.get("/organization/00000001a01d1c4c9395f80b")
if response.ok:
    print(response.json())
```

---

## 🔐 Environment Variables (for testing)

You can store credentials in a `.env` file for development/testing:

```
EMAIL=your@email.com
PASSWORD=yourpassword
TOTP_SECRET=yourtotpsecret
EPIC_DOMAIN=https://api-rv.epicio.com
```

---

## 🧪 Running Tests

First, install dev dependencies:

```bash
pipenv install --dev
```

Then you can run tests in either of the following ways:

### Option 1: Activate the shell

```bash
pipenv shell
pytest tests/
```

### Option 2: Run directly without shell

```bash
pipenv run pytest tests/
```

### Check that pytest is installed

To verify that `pytest` is installed in your virtualenv:

```bash
pipenv run which pytest
```

You should see something like:

```
/home/youruser/.local/share/virtualenvs/epic-rv-client-python-*/bin/pytest
```

---

## 📝 License

This project is maintained by Luis Lobo Borobia (<luis.lobo@epicio.com>) at [EPIC iO](https://www.epicio.com).
