#!/usr/bin/python3
from datetime import datetime, timedelta
import jwt
from flask_jwt_extended import JWTManager

# Set up JWT 
def setup_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)
    return jwt

# Create access token
def create_access_token(app, user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

