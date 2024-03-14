# Notes-Taking application using Flask and SQLAlchemy.
This API provides a comprehensive set of endpoints tailored to handle user authentication and note management tasks within your application. Whether you're developing a personal note-taking app or a collaborative workspace, these endpoints offer essential functionalities to enrich your users' experience.

## Required packages
```python
pip install requirements.txt
```

## API Endpoints

1. **Signup** - *POST*
   - The Signup endpoint accepts JSON payloads containing a username and password. It creates a new instance in the user database using the provided credentials.

2. **Login** - *POST*
   - The Login endpoint accepts JSON payloads containing a username and password. It validates the provided credentials. If the credentials are valid, it checks the username in the tokens database to retrieve a valid access token. If a valid token is found, it returns that token to the user. If not, a new token is generated, and any expired tokens are deleted from the database.

3. **Create Note** - *POST*
   - The Create Note endpoint requires an access token, message, and access list (a list of users who have access to the note, provided as a comma-separated string). If the token is valid, a new note is created in the database.

4. **Fetch Note** - *GET*
   - The Fetch Note endpoint requires a note ID and access token provided as JSON payloads. If the token is valid and the user associated with that token has access to the note, the note will be returned to the user. Otherwise, an appropriate error message will be displayed.

5. **Share Note** - *POST*
   - The Share Note endpoint requires a note ID, access token, and new usernames provided as JSON payloads. If the token is valid and the user associated with it has access to the note, the new usernames will be updated. Otherwise, an appropriate error message will be displayed.

6. **Update Note** - *PUT*
   - The Update Note endpoint requires a note ID, access token, and new message provided as JSON payloads. If the token is valid and the user associated with it has access to the note, the new message will be updated. Otherwise, an appropriate error message will be displayed.

   
## Testing
1. **Signup** - *POST*
``` cUrl
curl --location 'http://127.0.0.1:5000/signup' \
--header 'Content-Type: application/json' \
--data '{
    "username": "asdasdasd",
    "password": "123456",
}'
```
2. **Login** - *POST*
``` cUrl
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "asdasdasd",
    "password": "123456",
}'
```
3. **Create Note** - *POST*
``` cUrl
curl --location 'http://127.0.0.1:5000/notes/create' \
--header 'Content-Type: application/json' \
--data '{
    "access_token": "your-access-token",
    "access_list": "rsiva0400",
    "message": "Don'\''t die",
}'
```
4. **Fetch Note** - *GET*
``` cUrl
curl --location --request GET 'http://127.0.0.1:5000/notes/1' \
--header 'Content-Type: application/json' \
--data '{
    "access_token": "your-access-token",
}'
```  
5. **Share Note** - *POST*
```cUrl
curl --location 'http://127.0.0.1:5000/notes/share' \
--header 'Content-Type: application/json' \
--data '{
    "access_token": "your-access-token",
    "new_names": "asdasdasd,  ijonidnoinoind",
    "note_id": 6,
}'
```
6. **Update Note** - *PUT*
```cUrl
curl --location --request PUT 'http://127.0.0.1:5000/notes/1' \
--header 'Content-Type: application/json' \
--data '{
    "access_token": "your-access-token",
    "note_id": 6,
    "updated_text": "Don'\''t die (optional not a rule)"
}'
```

## Testing in Postman
For testing in Postman API, use the same api url and change the JSON payload with respect to API endpoint.


*JSON Payload for Fetch Note*
```
{
    "access_token": "your-access-token",
}
```
*Sample Output for Fetch Note*
```
{
    "access_list": [
        "rsiva0400",
        "newUser1",
        "newUser2"
    ],
    "created_by": "rsiva0400",
    "created_on": "2024-02-20 16:37:35",
    "id": 1,
    "message": "Hi, How are you?",
    "modified_by": "rsiva0400",
    "modified_on": "2024-02-20 16:37:35"
}
```
## Unit Testing - Pytest
For Unit testing, run **test_api_endpoint.py**.
```python
python -m pytest -v -s
```
