Notes-Taking application using Flask and SQLAlchemy.

Required packages
run pip install requirements.txt

**API Endpoints**

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

   
