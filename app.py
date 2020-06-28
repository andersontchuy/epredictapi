#! /usr/bin/env python
from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

dados = json.load(open('./data/alunos_ativos.json'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# rota para página de documentação da API
@app.route('/api-doc', methods=['GET'])
def show_doc():
    return render_template('document.html')

# consulta risco de evasão em todos os cursos
@app.route('/evasao', methods=['GET'])
def prever_evasao():
    return jsonify(dados)

# consulta risco de evasão por aluno
@app.route('/evasao/aluno/<int:matricula>', methods=['GET'])
def prever_evasao_aluno(matricula):
    for dado in dados:
        if dado['matricula'] == matricula:
            return jsonify(dado), 200
    return jsonify({'error': 'not found'}), 404

# consulta risco de evasão por curso
@app.route('/evasao/curso/<string:curso>', methods=['GET'])
def prever_evasao_por_curso(curso):
    curso_list = []
    for dado in dados:
        if dado['curso'].lower() == curso.lower():
            curso_list.append(dado)
    if len(curso_list) == 0:
        return jsonify({'error': 'not found'}), 404
    return jsonify(curso_list) 

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)