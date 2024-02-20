import pytest
import requests

@pytest.fixture
def api_url():
    return "http://127.0.0.1:5000"

@pytest.mark.parametrize("username, password, expected_status_code", [
    ("valid_username", "valid_password", 200),
    ("valid_username", "invalid_password", 400),
    ("", "", 400), 
])
def test_signup(api_url, username, password, expected_status_code):
    payload = {"username": username, "password": password}
    response = requests.post(api_url + "/signup", json=payload)
    
    assert response.status_code == expected_status_code

@pytest.mark.parametrize("username, password, expected_status_code", [
    ("valid_username", "valid_password", 200),
    ("valid_username", "invalid_password", 400),
    ("", "", 400), 
])
def test_login(api_url, username, password, expected_status_code):
    payload = {"username": username, "password": password}
    response = requests.post(api_url + "/login", json=payload)
    
    assert response.status_code == expected_status_code

def test_create_note(api_url):
    login_payload = {"username": 'valid_username', "password": 'valid_password'}
    login_response = requests.post(api_url + "/login", json=login_payload).json()

    access_token = login_response['access_token']
    create_note_payload = {"access_token": access_token, "message": 'Hi, How are you?', "access_list" : "newUser1,newUser2"}
    create_note_response = requests.post(api_url + "/notes/create", json=create_note_payload)

    assert create_note_response.status_code == 200

@pytest.mark.parametrize("note_id, expected_status_code", [
    (1, 200),
    (60, 400), 
])

def test_fetch_note(api_url, note_id, expected_status_code):
    login_payload = {"username": 'valid_username', "password": 'valid_password'}
    login_response = requests.post(api_url + "/login", json=login_payload).json()

    access_token = login_response['access_token']
    fetch_note_payload = {"access_token": access_token}

    fetch_note_response = requests.get(api_url + f'/notes/{note_id}', json=fetch_note_payload)

    assert fetch_note_response.status_code == expected_status_code
    print(fetch_note_response.json())

@pytest.mark.parametrize("note_id, updated_text,expected_status_code", [
    (2, 'i am fine',400),
    (1, 'a'*10, 200),
    (6, 'abcd',400), 
])

def test_update_note(api_url, note_id, updated_text, expected_status_code):
    login_payload = {"username": 'valid_username', "password": 'valid_password'}
    login_response = requests.post(api_url + "/login", json=login_payload).json()

    access_token = login_response['access_token']
    update_note_payload = {"access_token": access_token, 'updated_text': updated_text}

    update_note_response = requests.put(api_url + f'/notes/{note_id}', json=update_note_payload)
    print(update_note_response.json())
    assert update_note_response.status_code == expected_status_code
    



if __name__ == "__main__":
    pytest.main()
