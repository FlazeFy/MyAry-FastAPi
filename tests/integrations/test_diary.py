import requests
from datetime import datetime

base_url = "http://localhost:8000/api/v1"

# Dummy diary data
test_diary = {
    "diary_title": "Test Diary Title",
    "diary_desc": "Today I worked on testing the diary endpoint.",
    "diary_date": "2025-05-25T15:00:00",
    "diary_mood": 7,
    "diary_tired": 3
}

def test_create_diary():
    # Exec
    response = requests.post(f"{base_url}/diary", json=test_diary)
    data = response.json()

    # Check Default Response
    assert response.status_code == 201
    assert data['status'] == 'success'

    # Check String Keys
    list_string_keys = ['message', 'status']
    for key in list_string_keys:
        assert key in data
        assert isinstance(data[key], str), f"The key '{key}' should be a string"

    # Check Data Object
    assert 'data' in data
    assert isinstance(data['data'], dict)

    # Ensure All Diary Fields Are Returned
    for field in test_diary:
        assert field in data['data'], f"Missing field '{field}' in response"
        assert type(data['data'][field]) == type(test_diary[field]), f"Incorrect type for '{field}'"
