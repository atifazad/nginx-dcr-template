import hashlib
import random
import string

from flask import request
from flask import current_app as app
from .models import db, User, AuthToken
from datetime import datetime, timedelta

@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    response = None

    if username != None and password != None and email != None:

        try:

            existing_user = User.query.filter(
                User.username == username
            ).first()

            if existing_user == None:

                new_user = User(
                    username=username,
                    password=hashlib.sha256(str(password).encode('utf-8')).hexdigest(),
                    email=email,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )

                db.session.add(new_user)
                db.session.commit()
                print('NEW user ID: {}'.format(new_user.id))

                token = __generate_auth_token()
                __save_auth_token(new_user.id, token)
                print('Generated auth token successfully')

                response = {
                    'status': 'success',
                    'token': token,
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email
                }
            else:
                response = response = {
                    'status': 'failed',
                    'message': 'User {} already exists'.format(username)
                }

        except Exception as error:
            response = response = {
                'status': 'failed',
                'message': 'User registration failed. {}'.format(error)
            }

    return response

@app.route('/api/login', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    response = None
    try:
        authenticated = User.query.filter(
            User.username == username,
            User.password == hashlib.sha256(str(password).encode('utf-8')).hexdigest()
        ).first()

        if authenticated != None:

            token = __generate_auth_token()

            if len(authenticated.auth_tokens) > 0:
                token = authenticated.auth_tokens[0].token if authenticated.auth_tokens[0].expires_at <= datetime.now() \
                    else authenticated.auth_tokens[0].token
            else:
                __save_auth_token(authenticated.id, token)

            response = {
                'status': 'success',
                'token': token,
                'id': authenticated.id,
                'username': authenticated.username,
                'email': authenticated.email
            }
        else:
            response = {
                'status': 'failed',
                'message': 'Login failed'
            }
    except Exception as error:
        response = {
            'status': 'failed',
            'message': 'An error occured: {}'.format(error)
        }

    return response

def __generate_auth_token():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])

def __save_auth_token(user_id, token):
    auth_token = AuthToken(
        user_id=user_id,
        token=token,
        expires_at= datetime.now() + timedelta(seconds=app.config.get('SESSION_LENGTH')),
        created_at=datetime.now()
    )

    db.session.add(auth_token)
    db.session.commit()
