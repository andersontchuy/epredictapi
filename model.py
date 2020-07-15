#coding: utf-8
import pickle
import json
from normalize import normalizaDados

evasion = pickle.load(open('./modelo/evasao_modelo_v3.0.sav','rb'))
lista = json.load(open('./data/alunos_ativos.json'))

def preveEvasao(aluno):
   result = evasion.predict(aluno.reshape(1, -1))
   return result

def calculaProbabilidade(aluno):
   prob = evasion.predict_proba(aluno.reshape(1, -1))
   result  = int(round(prob[0][1]*100, 0))
   return result

def listaAlunoPredito(lista):
   lista_aluno = {}
   for aluno in range(len(lista)):
      predicao = preveEvasao(lista[aluno])
      if predicao == 'sim':
         lista_aluno[aluno] = lista[aluno]
   return lista_aluno

def listaAlunoPorCurso(lista, curso):
    lista_aluno = []
    [lista_aluno.append(dado) for dado in lista if dado['curso'] == curso]
    return lista_aluno

def separaAlunoPorCurso(lista):
   cc, es, si = [], [], []
   evasao = lambda x: cc.append(lista[0]) if x == 1 else (
      es.append(lista[0]) if x == 2 else si.append(lista[0]))
   for curso in lista:
      evasao(curso[0])
   return cc, es, si

def mostraPredicaoGeral(lista):
   nlista = normalizaDados(lista)
   alunos = listaAlunoPredito(nlista)
   cc, es, si = separaAlunoPorCurso(nlista) # todos os alunos
   qcc = len(cc)
   qes = len(es)
   qsi = len(si)
   cc, es, si = [], [], []
   cc, es, si = separaAlunoPorCurso(list(alunos.values())) # alunos preditos
   qecc = len(cc)
   qees = len(es)
   qesi = len(si)
   qat = len(lista)
   qet = len(alunos)

   result = {
      'quant_aluno_cc': str(qcc),
      'quant_aluno_es': str(qes),
      'quant_aluno_si': str(qsi),
      'quant_aluno_total': str(qat),
      'quant_evasao_cc': str(qecc),
      'quant_evasao_es': str(qees),
      'quant_evasao_si': str(qesi), 
      'quant_evasao_total': str(qet), 
      'percent_evasao_cc': str(int(round((qecc/qet) * 100, 0))),
      'percent_evasao_es': str(int(round((qees/qet) * 100, 0))),
      'percent_evasao_si': str(int(round((qesi/qet) * 100, 0))),
      'percent_evasao_total': str(int(round((qet/qat)*100, 0)))
      }
   return result

def mostraPredicaoPorCurso(lista, id_curso):
   if id_curso == 'a' or id_curso == 'cc':
      curso = 'CIÊNCIA DA COMPUTAÇÃO'
   elif id_curso == 'b' or id_curso == 'es':
      curso = 'ENGENHARIA DE SOFTWARE'
   elif id_curso == 'c' or id_curso == 'si':
      curso = 'SISTEMAS DE INFORMAÇÃO'
   else:
      return 0

   nlista = normalizaDados(lista)
   lista_predicao = listaAlunoPredito(nlista)
   lista_aluno_predito = []
   [lista_aluno_predito.append(lista[key]) for key in lista_predicao.keys()]  
   lista_aluno_predito_curso = listaAlunoPorCurso(lista_aluno_predito, curso)

   total_aluno_curso = len(listaAlunoPorCurso(lista, curso))
   total_evasao = len(lista_aluno_predito_curso)
   percentual = int(round((total_evasao/total_aluno_curso) * 100, 0))

   dado_aluno = []
   for dado in lista_aluno_predito_curso:
      dado_aluno.append({
         'matricula': str(dado['matricula']),
         'turno': dado['turno'],
         'forma_ingresso': dado['forma_ingresso'],
         'ano_ingresso': str(dado['ano_ingresso']),
         'sexo': dado['sexo'],
         'cor_raca': dado['cor_raca'],
         'percentual_integralizado': str(dado['percentual_integralizado']),
         'escola_publica': dado['escola_publica']
      })

   result = {
      'total_aluno': str(total_aluno_curso),
      'total_evasao': str(total_evasao),
      'percentual_evasao': str(percentual),
      'lista_aluno': dado_aluno
   }
   
   return result

def mostraPredicaoAluno(matricula):
   aluno = []
   [aluno.append(dado) for dado in lista if dado['matricula'] == matricula]
   
   if len(aluno) == 0:
      return 0     

   ndado = normalizaDados(aluno)
   predicao = preveEvasao(ndado)
   prob = calculaProbabilidade(ndado)

   result = {
      'status': predicao[0],
      'probabilidade_evasao': str(prob),
      'curso': aluno[0]['curso'],
      'grau_academico': aluno[0]['grau_academico'],
      'modalidade': aluno[0]['modalidade'],
      'turno': aluno[0]['turno'],
      'forma_ingresso': aluno[0]['forma_ingresso'],
      'especificidade_ingresso': aluno[0]['especificidade_ingresso'],
      'categoria_ingresso': aluno[0]['categoria_ingresso'],
      'ano_ingresso': str(aluno[0]['ano_ingresso']),
      'semestre_ingresso': str(aluno[0]['semestre_ingresso']),
      'sexo': aluno[0]['sexo'],
      'cor_raca': aluno[0]['cor_raca'],
      'deficiencia': aluno[0]['deficiencia'],
      'media_global_aluno': str(aluno[0]['media_global_aluno']),
      'media_global_curso': str(aluno[0]['media_global_curso']),
      'percentual_integralizado': str(aluno[0]['percentual_integralizado']),
      'escola_publica': aluno[0]['escola_publica'],
      'escola_ensino_medio': aluno[0]['escola_ensino_medio'],
      'cidade_endereco': aluno[0]['cidade_endereco'],
      'uf_endereco': aluno[0]['uf_endereco'],
      'total_trancamentos': str(aluno[0]['total_trancamentos'])
   }

   return result
