import jwt
import datetime
import functools
from config import SECRET_KEY
from users import usuario_por_email, checa_senha
from flask import request, jsonify, session

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': {}}), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = usuario_por_email(email=data['username'])
        except:
            return jsonify({
                'message': 'token is invalid or expired',
                'data': {}}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({
            'message': 'could not verify', 
            'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = usuario_por_email(auth.username)
    if not user:
        return jsonify({'message': 'user not found', 'data': {}}), 401 

    if user and checa_senha(user['senha'], auth.password):
        token = jwt.encode({
            "username": user['email'], 
            "exp": datetime.datetime.now() + datetime.timedelta(hours=12)}, 
            SECRET_KEY)
        return jsonify({
            'message': 'Validated successfully', 
            'token': token.decode('UTF-8'),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})
    
    return jsonify({
            'message': 'could not verify', 
            'WWW-Authenticate': 'Basic auth="Login required"'}), 401
    
    