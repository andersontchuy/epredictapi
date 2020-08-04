#coding: utf-8
import os
import helper
from flask_cors import CORS
from flask_sslify import SSLify
from flask_compress import Compress
from flask import Flask, jsonify, render_template, request, redirect
from model import mostraPredicaoGeral, mostraPredicaoPorCurso, mostraPredicaoAluno

app = Flask(__name__)
app.config.from_object('config')
CORS(app, supports_credentials=True)
Compress(app)
SSLify(app, permanent=True)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# rota página de documentação da API
@app.route('/api-doc', methods=['GET'])
def show_doc():
    return render_template('document.html')

@app.route('/auth', methods=['POST'])
def autenticacao():
    return helper.auth()

# rota predição de evasão todos os cursos
@app.route('/evasao/', methods=['GET'])
@helper.token_required
def prever_evasao(current_user):
    result = mostraPredicaoGeral()
    result['usuario'] = current_user['nome']
    return jsonify(result), 200

# rota predição de evasão por curso
@app.route('/evasao/curso/<string:curso>', methods=['GET'])
@helper.token_required
def prever_evasao_por_curso(current_user, curso):
    result = mostraPredicaoPorCurso(curso)
    if result == 0:
        return jsonify({'error': 'not found'}), 404
    result['usuario'] = current_user['nome']
    return jsonify(result), 200

# rota predição de evasão por aluno
@app.route('/evasao/aluno/<int:matricula>', methods=['GET'])
@helper.token_required
def prever_evasao_aluno(current_user, matricula):
    result = mostraPredicaoAluno(matricula)
    if result == 0:
        return jsonify({'error': 'not found'}), 404
    result['usuario'] = current_user['nome']
    return jsonify(result), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)