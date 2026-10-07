import pytest

from utils.data_factory import booking_payload


def test_get_non_existent_booking_returns_404(client):
    assert client.get_booking(999999999).status_code == 404


@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "invalid-token"])
def test_update_requires_valid_token(client, booking, token):
    booking_id, original = booking

    response = client.update_booking(booking_id, booking_payload(firstname="Hacker"), token)
    assert response.status_code == 403
    assert client.get_booking(booking_id).json() == original  # data unchanged


@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "invalid-token"])
def test_delete_requires_valid_token(client, booking, token):
    booking_id, _ = booking

    assert client.delete_booking(booking_id, token).status_code == 403
    assert client.get_booking(booking_id).status_code == 200  # still exists


@pytest.mark.xfail(strict=True, reason="DEFECT: missing required fields cause 500 Internal Server Error; expected 400 Bad Request")
def test_create_with_missing_fields_returns_400(client):
    response = client.create_booking({"firstname": "OnlyFirstName"})
    assert response.status_code == 400
