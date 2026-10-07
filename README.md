# REST API Test Automation Framework — PyTest

[![API Tests](https://github.com/AlAmin870/qa-pytest-api-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/AlAmin870/qa-pytest-api-framework/actions/workflows/api-tests.yml)

A modular API testing framework built with **Python, PyTest, Requests and JSON Schema**, testing the [Restful Booker](https://restful-booker.herokuapp.com/apidoc/index.html) hotel-booking API. It covers token authentication, full CRUD, negative and security checks, and runs on GitHub Actions on every push and weekly on a schedule.

## Results

**17 tests — 15 passed, 2 known defects documented**

| Area | What's tested |
|---|---|
| Auth | Health check, token generation, rejection of bad credentials |
| CRUD | Create, read, filter by name, full update (PUT), partial update (PATCH), delete |
| Chained flow | Create → read → update → delete → confirm 404, in one test |
| Negative / security | 404 for unknown IDs; update and delete blocked without a token or with an invalid token, and data verified unchanged |
| Contract | Every response validated against a JSON Schema |
| Performance | Response time asserted under a configurable limit |

### Defects found

Both are kept in the suite as `xfail(strict=True)` tests, so CI flags it the day they are fixed.

| # | Endpoint | Expected | Actual | Severity |
|---|---|---|---|---|
| 1 | `POST /auth` with wrong password | `401 Unauthorized` | `200 OK` with `{"reason": "Bad credentials"}` | Medium: clients can't rely on the status code to detect failed login |
| 2 | `POST /booking` with missing required fields | `400 Bad Request` with a validation message | `500 Internal Server Error` | High: unhandled server error instead of input validation |

## Framework design

```
├── clients/booking_client.py   # API wrapper: one method per endpoint, request/response logging
├── schemas/booking_schemas.py  # JSON Schemas for contract validation
├── utils/data_factory.py       # Builds unique test data so runs never collide
├── tests/
│   ├── test_auth.py
│   ├── test_booking_crud.py
│   └── test_booking_negative.py
├── conftest.py                 # Session client, auth token, booking fixture with auto-cleanup
├── config.py                   # Base URL, credentials, limits (all overridable by env vars)
└── .github/workflows/api-tests.yml
```

- **Client layer:** tests never build URLs or headers by hand.
- **Fixtures with teardown:** every booking a test creates is deleted afterwards.
- **Data factory:** unique names per run, with overrides for specific cases.
- **Config via environment variables:** point the same suite at another environment with `BASE_URL=...`.
- **Markers:** `pytest -m smoke` runs the quick health checks only.
- **Reporting:** HTML report at `reports/report.html`, uploaded by CI as an artifact.

## Run locally

```bash
pip install -r requirements.txt
pytest                # full suite
pytest -m smoke       # smoke tests only
```
