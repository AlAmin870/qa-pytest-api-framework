import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")

# Public demo credentials documented by Restful Booker; override via env vars
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "password123")

# Upper bound for a single request, used by the response-time checks
MAX_RESPONSE_SECONDS = float(os.getenv("MAX_RESPONSE_SECONDS", "5"))
