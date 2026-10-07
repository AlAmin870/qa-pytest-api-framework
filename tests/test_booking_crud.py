import pytest
from jsonschema import validate

import config
from schemas.booking_schemas import BOOKING, BOOKING_IDS, CREATED_BOOKING
from utils.data_factory import booking_payload


@pytest.mark.smoke
def test_create_booking(client, token):
    payload = booking_payload()
    response = client.create_booking(payload)

    assert response.status_code == 200
    body = response.json()
    validate(body, CREATED_BOOKING)
    assert body["booking"] == payload
    assert response.elapsed.total_seconds() < config.MAX_RESPONSE_SECONDS

    client.delete_booking(body["bookingid"], token)


def test_get_booking_returns_saved_data(client, booking):
    booking_id, payload = booking
    response = client.get_booking(booking_id)

    assert response.status_code == 200
    validate(response.json(), BOOKING)
    assert response.json() == payload


def test_list_bookings_filtered_by_name(client, booking):
    booking_id, payload = booking
    response = client.list_bookings(firstname=payload["firstname"], lastname=payload["lastname"])

    assert response.status_code == 200
    validate(response.json(), BOOKING_IDS)
    assert {"bookingid": booking_id} in response.json()


def test_full_update_with_put(client, token, booking):
    booking_id, _ = booking
    updated = booking_payload(firstname="Updated", totalprice=999, depositpaid=False)

    response = client.update_booking(booking_id, updated, token)
    assert response.status_code == 200
    assert response.json() == updated
    assert client.get_booking(booking_id).json() == updated


def test_partial_update_with_patch(client, token, booking):
    booking_id, original = booking

    response = client.patch_booking(booking_id, {"totalprice": 75}, token)
    assert response.status_code == 200
    assert response.json()["totalprice"] == 75
    # Fields not sent in the PATCH must stay unchanged
    assert response.json()["lastname"] == original["lastname"]


def test_delete_booking(client, token, booking):
    booking_id, _ = booking

    assert client.delete_booking(booking_id, token).status_code == 201
    assert client.get_booking(booking_id).status_code == 404


def test_end_to_end_booking_lifecycle(client, token):
    """Create -> read -> update -> delete -> confirm gone, in one chained flow."""
    payload = booking_payload()
    booking_id = client.create_booking(payload).json()["bookingid"]

    assert client.get_booking(booking_id).json() == payload

    client.patch_booking(booking_id, {"additionalneeds": "Late checkout"}, token)
    assert client.get_booking(booking_id).json()["additionalneeds"] == "Late checkout"

    client.delete_booking(booking_id, token)
    assert client.get_booking(booking_id).status_code == 404
