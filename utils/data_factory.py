import uuid
from datetime import date, timedelta


def booking_payload(**overrides):
    """Build a valid booking with a unique last name so test runs never collide."""
    checkin = date.today() + timedelta(days=30)
    payload = {
        "firstname": "QA",
        "lastname": f"Test-{uuid.uuid4().hex[:8]}",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": (checkin + timedelta(days=3)).isoformat(),
        },
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload
