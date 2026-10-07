import requests

from utils.logger import logger


class BookingClient:
    """Thin wrapper around the Restful Booker API.

    Tests call methods like client.create_booking(payload) instead of building
    URLs and headers by hand, so an endpoint change is fixed in one place.
    """

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.session.hooks["response"].append(self._log)

    @staticmethod
    def _log(response, *args, **kwargs):
        req = response.request
        logger.info("%s %s -> %s (%.0f ms)", req.method, req.url,
                    response.status_code, response.elapsed.total_seconds() * 1000)
        logger.debug("Response body: %s", response.text[:500])

    @staticmethod
    def _auth(token):
        return {"Cookie": f"token={token}"} if token else {}

    # --- Auth / health -------------------------------------------------------
    def ping(self):
        return self.session.get(f"{self.base_url}/ping")

    def create_token(self, username, password):
        return self.session.post(f"{self.base_url}/auth",
                                 json={"username": username, "password": password})

    # --- Bookings ------------------------------------------------------------
    def list_bookings(self, **filters):
        return self.session.get(f"{self.base_url}/booking", params=filters)

    def get_booking(self, booking_id):
        return self.session.get(f"{self.base_url}/booking/{booking_id}")

    def create_booking(self, payload):
        return self.session.post(f"{self.base_url}/booking", json=payload)

    def update_booking(self, booking_id, payload, token=None):
        return self.session.put(f"{self.base_url}/booking/{booking_id}",
                                json=payload, headers=self._auth(token))

    def patch_booking(self, booking_id, fields, token=None):
        return self.session.patch(f"{self.base_url}/booking/{booking_id}",
                                  json=fields, headers=self._auth(token))

    def delete_booking(self, booking_id, token=None):
        return self.session.delete(f"{self.base_url}/booking/{booking_id}",
                                   headers=self._auth(token))
