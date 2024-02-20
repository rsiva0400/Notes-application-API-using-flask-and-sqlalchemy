from flask import Flask, request, jsonify
from database import *


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'tokens': 'sqlite:///tokens.db',
    'notes': 'sqlite:///notes.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "i_am_ironman"  

init_db(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    if get_user_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400
    create_user(username, password)
    return jsonify({'message': 'User created successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = get_user_by_username(username)
    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password'}), 400
    token = get_token_by_username(username)
    if token:
        return jsonify({'access_token': token.token})

    token = create_access_token(username)
    delete_expired_tokens()
    return jsonify({
        'access_token': token,
        'message': 'This token will be expired in 5 minutes.'
        }), 200

# Create notes
@app.route('/notes/create', methods=['POST'])
def create_note():
    data = request.get_json()
    message = data.get('message')
    access_token = data.get('access_token')
    access_list = data.get('access_list')

    if validate_token(access_token):
        note_id = create_new_note(
            message=message, 
            created_by=get_access_token(access_token).username,
            access_list=access_list
            )
        return jsonify({'response':'Note created successfully', 'note_id': note_id}), 200
        
    else:
        return jsonify({'response':'Invalid or expried access token.'}), 400

@app.route('/notes/<int:id>', methods=['GET'])
def fetch_note(id):
    data = request.get_json()
    access_token = data.get('access_token')
    if validate_token(access_token):
        return get_note(id, access_token)
    else:
        return jsonify({'response':'Invalid or expried access token. Login again.'}), 400

@app.route('/notes/share', methods=['POST'])
def share_note():
    data = request.get_json()
    access_token = data.get('access_token')
    note_id = data.get('note_id')
    new_names = data.get('new_names')
    if validate_token(access_token):
        return share_note_access(note_id, access_token, new_names)
    else:
        return jsonify({'response':'Invalid or expried access token. Login again.'}), 400

@app.route('/notes/<int:id>', methods = ['PUT'])
def update_note(id):
    data = request.get_json()
    access_token = data.get('access_token')
    note_id = data.get('note_id')
    updated_text = data.get('updated_text')
    if validate_token(access_token):
        return update_note_func(note_id, access_token, updated_text)
    else:
        return jsonify({'response':'Invalid or expried access token. Login again.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
