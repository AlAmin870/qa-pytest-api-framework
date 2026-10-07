BOOKING = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string", "format": "date"},
                "checkout": {"type": "string", "format": "date"},
            },
        },
        "additionalneeds": {"type": "string"},
    },
}

CREATED_BOOKING = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING,
    },
}

BOOKING_IDS = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["bookingid"],
        "properties": {"bookingid": {"type": "integer"}},
    },
}

TOKEN = {
    "type": "object",
    "required": ["token"],
    "properties": {"token": {"type": "string", "minLength": 1}},
}
