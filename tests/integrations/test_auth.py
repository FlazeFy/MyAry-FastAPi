import requests

base_url = "http://localhost:8000/api/v1" 

# Dummy test user
test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "test123"
}

def test_register_user():
    # Exec
    response = requests.post(f"{base_url}/auth/register", json=test_user)
    data = response.json()

    # Check Default Response
    assert response.status_code == 200
    assert data['status'] == 'success'

    # Check String Object
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"

def test_login_user():
    # Test Data
    payload = {
        "username": test_user["username"],
        "password": test_user["password"]
    }

    # Exec
    response = requests.post(f"{base_url}/auth/login", json=payload)
    data = response.json()

    # Check Default Response
    assert response.status_code == 200
    assert data['status'] == 'success'

    # Check String Object
    list_string_object = ['message','status','refresh_token','access_token']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"

def test_refresh_auth_token():
    # Test Data
    payload = {
        "username": test_user["username"],
        "password": test_user["password"]
    }

    # Exec - Login
    response = requests.post(f"{base_url}/auth/login", json=payload)
    data_login = response.json()

    if response.status_code == 200:
        # Test Data
        refresh_token = data_login['refresh_token']
        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }
        # Exec - Login
        response = requests.post(f"{base_url}/auth/refresh", headers=headers)
        data = response.json()

        # Check String Object
        list_string_object = ['message','status','access_token']
        for col in list_string_object:
            assert col in data
            assert isinstance(data[col], str), f"The key '{col}' should be a string"
