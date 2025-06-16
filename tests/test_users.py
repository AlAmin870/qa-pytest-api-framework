import requests

def test_get_users(auth_token, base_url):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{base_url}/users", headers=headers)
    assert response.status_code == 200
    assert "users" in response.json()