import pytest
import requests

@pytest.fixture
def base_url():
    return "https://api.example.com"

@pytest.fixture
def auth_token(base_url):
    payload = {"username": "admin", "password": "123456"}
    response = requests.post(f"{base_url}/login", json=payload)
    return response.json()["token"]