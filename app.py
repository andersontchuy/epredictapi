#! /usr/bin/env python
import json, random, os
from flask import Flask, jsonify, render_template, request
from model import mostraPredicaoGeral
from model import mostraPredicaoPorCurso

app = Flask(__name__)

# dados atualizados em: 07.07.2020
dados = json.load(open('./data/alunos_ativos.json'))

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
    result = mostraPredicaoGeral(dados)
    return jsonify(result), 200

# rota predição de evasão por aluno
@app.route('/evasao/aluno/<int:matricula>', methods=['GET'])
def prever_evasao_aluno(matricula):
    for dado in dados:
        if dado['matricula'] == matricula:
            return jsonify({
                'curso': dado['curso'],
                'turno': dado['turno'],
                'forma_ingresso': dado['forma_ingresso'],
                'especificidade_ingresso': dado['especificidade_ingresso'],
                'categoria_ingresso': dado['categoria_ingresso'],
                'ano_ingresso': str(dado['ano_ingresso']),
                'semestre_ingresso': str(dado['semestre_ingresso']),
                'sexo': dado['sexo'],
                'cor_raca': dado['cor_raca'],
                'deficiencia': dado['deficiencia'],
                'dt_nascimento': dado['dt_nascimento'],
                'score': str(round(random.random(), 4)), 
                'media_global_curso': str(dado['media_global_curso']),
                'media_global_aluno': str(dado['media_global_aluno']),
                'percentual_integralizado': str(dado['percentual_integralizado']),
                'escola_publica': dado['escola_publica'],
                'cidade_endereco': dado['cidade_endereco'],
                'uf_endereco': dado['uf_endereco'],
                'total_trancamentos': str(dado['total_trancamentos']),
                'possui_tracamento_compulsorio': dado['possui_tracamento_compulsorio']
            }), 200
    return jsonify({'error': 'not found'}), 404

# rota predição de evasão por curso
@app.route('/evasao/curso/<string:curso>', methods=['GET'])
def prever_evasao_por_curso(curso):
    result = mostraPredicaoPorCurso(dados, curso)
    if result == 0:
        return jsonify({'error': 'not found'}), 404
    return jsonify(result), 200


# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)