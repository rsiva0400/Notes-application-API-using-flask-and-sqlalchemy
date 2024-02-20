import secrets
from models import db, User, AccessToken, Notes
from datetime import datetime, timedelta
from flask import jsonify

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# User data functions
def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


# Access token funtions

def get_token_by_username(username):
    return AccessToken.query.filter_by(username=username).first()

def create_access_token(username):
    token = secrets.token_hex(16)
    expiry_time = datetime.now() + timedelta(minutes=5)
    try:
        access_token = AccessToken(token=token, expiry_time=expiry_time, username=username)
        db.session.add(access_token)
        db.session.commit()
        return token
    except:
        create_access_token(username)
def validate_token(token):
    token =  AccessToken.query.filter_by(token=token).first()

    if not token:
        return False
    
    if token.expiry_time < datetime.now():
        db.session.delete(token)
        db.session.commit()
        return False
    return True


def get_access_token(token):
    return AccessToken.query.filter_by(token=token).first()

def delete_access_token(token):
    access_token = AccessToken.query.filter_by(token=token).first()
    if access_token:
        db.session.delete(access_token)
        db.session.commit()

def delete_expired_tokens():
    expired_tokens = AccessToken.query.filter(AccessToken.expiry_time < datetime.now()).all()
    for token in expired_tokens:
        db.session.delete(token)
    db.session.commit()

# notes CRUD operations
def create_new_note(message, created_by,access_list):
    note = Notes(
        message = message, 
        created_on = datetime.now(),
        modified_on = datetime.now(),
        created_by = created_by, 
        modified_by = created_by, 
        access_list = created_by + ',' +access_list
        )
    db.session.add(note)
    db.session.commit()
    return note.id

def get_note(id, access_token):
    note =  note =  Notes.query.get(id)
    if not note:
        return jsonify({'response':'Note Id is Invalid.'}), 400
    user = get_access_token(access_token).username
    access_list = note.access_list.split(',')
    if user in access_list:
        return jsonify(note.to_dict()),200
    else:
        return jsonify({'response':"You don't have access to this note."}), 400
        
    
def share_note_access(id, access_token, new_names):
    note =  Notes.query.get(id)
    if not note:
        return jsonify({'response':'Note Id is Invalid.'}), 400
    
    user = get_access_token(access_token).username
    access_list = note.access_list.split(',')
    if user != note.created_by:
        return jsonify({'response':"You don't have access to this note. Only admin can share this note"}), 400
    
    new_names = new_names.split(',')
    new_names = [i.strip() for i in new_names]
    access_list.extend(new_names)
    note.access_list = ','.join(set(access_list))
    db.session.commit()
    return jsonify({'response':"Successfully shared access."}), 200
        
    
def update_note_func(id, access_token, updated_text):
    note =  Notes.query.get(id)
    if not note:
        return jsonify({'response':'Note Id is Invalid.'}), 400

    user = get_access_token(access_token).username
    access_list = note.access_list.split(',')
    if user not in access_list:
        return jsonify({'response':"You don't have access to this note."}), 400
    
    if len(updated_text) > 1000:
        return jsonify({'response':"Message can only have 1000 characters."}), 400
    
    note.message = updated_text
    note.modified_on = datetime.now()
    note.modified_by = user
    db.session.commit()
    return jsonify({'response':"Successfully updated."}), 200
