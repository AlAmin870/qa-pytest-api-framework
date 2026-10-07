import pytest
from jsonschema import validate

import config
from schemas.booking_schemas import TOKEN


@pytest.mark.smoke
def test_health_check(client):
    assert client.ping().status_code == 201


@pytest.mark.smoke
def test_valid_credentials_return_token(client):
    response = client.create_token(config.USERNAME, config.PASSWORD)
    assert response.status_code == 200
    validate(response.json(), TOKEN)


def test_invalid_credentials_are_rejected(client):
    response = client.create_token(config.USERNAME, "wrong-password")
    assert response.json() == {"reason": "Bad credentials"}
    assert "token" not in response.json()


@pytest.mark.xfail(strict=True, reason="DEFECT: API returns 200 OK for bad credentials; expected 401 Unauthorized")
def test_invalid_credentials_return_401(client):
    response = client.create_token(config.USERNAME, "wrong-password")
    assert response.status_code == 401
