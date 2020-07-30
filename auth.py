import functools
import json
from flask import Blueprint, redirect, request, session, jsonify
from users import busca_usuario

auth = Blueprint("auth",__name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'nome' in session.keys():
            return jsonify({'message': 'could not verify', 
            'WWW-Authenticate': 'Basic auth="Login required"'}), 401
        return view(**kwargs)
    return wrapped_view

@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        email = ''
        senha = ''
        if request.method == 'POST':
            email = request.get_json(force=True)["email"]
            senha = request.get_json(force=True)["senha"]
        elif request.args["email"] == "teste@ies.br":
            email = request.args["email"]
            senha = request.args["senha"]
        
    except Exception as e:
        print(e)
        return jsonify({'message': 'user not found'}), 404

    usuario =  busca_usuario(email, senha)

    if not usuario:
        return jsonify({'message': 'user not found'}), 404

    session['nome'] = usuario[0]
    # return 'usuario :%s'%session['nome']
    return jsonify({'status': 'conectado'}), 200


@auth.route('/logout')
def logout():
    session.clear()

    return jsonify({'status': 'desconectado'}), 200