import pytest

import config
from clients.booking_client import BookingClient
from utils.data_factory import booking_payload


@pytest.fixture(scope="session")
def client():
    return BookingClient(config.BASE_URL)


@pytest.fixture(scope="session")
def token(client):
    response = client.create_token(config.USERNAME, config.PASSWORD)
    assert response.status_code == 200, response.text
    return response.json()["token"]


@pytest.fixture
def booking(client, token):
    """Create a fresh booking for one test and delete it afterwards."""
    payload = booking_payload()
    response = client.create_booking(payload)
    assert response.status_code == 200, response.text
    booking_id = response.json()["bookingid"]
    yield booking_id, payload
    client.delete_booking(booking_id, token)  # cleanup; ignored if the test already deleted it
