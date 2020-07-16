#coding: utf-8
import os
from flask import Flask, jsonify, render_template, request
from model import mostraPredicaoGeral, mostraPredicaoPorCurso, mostraPredicaoAluno

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# rota página de documentação da API
@app.route('/api-doc', methods=['GET'])
def show_doc():
    return render_template('document.html')

# rota predição de evasão todos os cursos
@app.route('/evasao/', methods=['GET'])
def prever_evasao():
    result = mostraPredicaoGeral()
    return jsonify(result), 200

# rota predição de evasão por curso
@app.route('/evasao/curso/<string:curso>', methods=['GET'])
def prever_evasao_por_curso(curso):
    result = mostraPredicaoPorCurso(curso)
    if result == 0:
        return jsonify({'error': 'not found'}), 404
    return jsonify(result), 200

# rota predição de evasão por aluno
@app.route('/evasao/aluno/<int:matricula>', methods=['GET'])
def prever_evasao_aluno(matricula):
    result = mostraPredicaoAluno(matricula)
    if result == 0:
        return jsonify({'error': 'not found'}), 404
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)