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
   result  = round(prob[0][1]*100, 2)
   return result

def listaAlunoPredito(lista):
   lista_aluno = {}
   for aluno in range(len(lista)):
      predicao = preveEvasao(lista[aluno])
      if predicao == 'sim':
         lista_aluno[aluno] = calculaProbabilidade(lista[aluno])
   return lista_aluno

def listaAlunoPorCurso(lista, curso):
   lista_aluno = [dado for dado in lista if dado['curso'] == curso]
   return lista_aluno

def mostraPredicaoGeral():
   cc, es, si = '', '', ''
   cc = listaAlunoPorCurso(lista, 'CIÊNCIA DA COMPUTAÇÃO')
   es = listaAlunoPorCurso(lista, 'ENGENHARIA DE SOFTWARE')
   si = listaAlunoPorCurso(lista, 'SISTEMAS DE INFORMAÇÃO' )

   ncc = normalizaDados(cc)
   nes = normalizaDados(es)
   nsi = normalizaDados(si)

   # quantidade de alunos por curso
   qcc = len(ncc)
   qes = len(nes)
   qsi = len(nsi)

   pcc = listaAlunoPredito(ncc)
   pes = listaAlunoPredito(nes)
   psi = listaAlunoPredito(nsi)

   # quantidade de alunos com predição de evasão por curso
   qecc = len(pcc)
   qees = len(pes)
   qesi = len(psi)
   
   qat = qcc + qes + qsi      # total de alunos
   qet = qecc + qees + qesi   # total de predição de evasão

   result = {
      'curso_percent': [
         {
            'curso': "Ciências da Computação",
            'quant_aluno': qcc,
            'percent_evasao': int(round((qecc/qet) * 100, 0)),
            'quant_evasao': qecc
         },
         {
            'curso': "Engenharia de Software",
            'quant_aluno': qes,
            'percent_evasao': int(round((qees/qet) * 100, 0)),
            'quant_evasao': qees
         },
         {
            'curso': "Sistemas de Informação",
            'quant_aluno': qsi,
            'percent_evasao': int(round((qesi/qet) * 100, 0)),
            'quant_evasao': qesi, 
         }
      ],
      'quant_aluno_total': qat,
      'quant_evasao_total': qet,
      'percent_evasao_total': int(round((qet/qat) * 100, 0)) 
   }  

   return result

def mostraPredicaoPorCurso(id_curso):
   curso = ''
   if id_curso == 'a' or id_curso == 'cc':
      curso = 'CIÊNCIA DA COMPUTAÇÃO'
   elif id_curso == 'b' or id_curso == 'es':
      curso = 'ENGENHARIA DE SOFTWARE'
   elif id_curso == 'c' or id_curso == 'si':
      curso = 'SISTEMAS DE INFORMAÇÃO'
   else:
      return 0

   lista_aluno = listaAlunoPorCurso(lista, curso)
   nlista = normalizaDados(lista_aluno)
   lista_predicao = listaAlunoPredito(nlista) 
   lista_aluno_predito = []
   for key, value in lista_predicao.items():
      lista_aluno[key]['probabilidade_evasao'] = value
      lista_aluno_predito.append(lista_aluno[key])

   total_aluno_curso = len(lista_aluno)
   total_evasao = len(lista_aluno_predito)
   percentual = int(round((total_evasao/total_aluno_curso) * 100, 0))

   dado_aluno = []
   for dado in lista_aluno_predito:
      dado_aluno.append({
         'matricula': str(dado['matricula']),
         'probabilidade_evasao': dado['probabilidade_evasao'],
         'turno': dado['turno'],
         'forma_ingresso': dado['forma_ingresso'],
         'ano_ingresso': dado['ano_ingresso'],
         'sexo': dado['sexo'],
         'cor_raca': dado['cor_raca'],
         'percentual_integralizado': dado['percentual_integralizado'],
         'escola_publica': dado['escola_publica'],
         'cidade_endereco': dado['cidade_endereco'],
         'media_global_aluno': dado['media_global_aluno'],
         'media_global_curso': dado['media_global_curso']
      })

   result = {
      'total_aluno': str(total_aluno_curso),
      'total_evasao': str(total_evasao),
      'percentual_evasao': str(percentual),
      'lista_aluno': dado_aluno
   }
   
   return result

def mostraPredicaoAluno(matricula):
   aluno = ''
   aluno = [dado for dado in lista if dado['matricula'] == matricula]
   
   if len(aluno) == 0:
      return 0     

   ndado = normalizaDados(aluno)
   predicao = preveEvasao(ndado)
   prob = calculaProbabilidade(ndado)

   result = {
      'status': predicao[0],
      'probabilidade_evasao': prob,
      'curso': aluno[0]['curso'],
      'grau_academico': aluno[0]['grau_academico'],
      'modalidade': aluno[0]['modalidade'],
      'turno': aluno[0]['turno'],
      'forma_ingresso': aluno[0]['forma_ingresso'],
      'especificidade_ingresso': aluno[0]['especificidade_ingresso'],
      'categoria_ingresso': aluno[0]['categoria_ingresso'],
      'ano_ingresso': aluno[0]['ano_ingresso'],
      'semestre_ingresso': aluno[0]['semestre_ingresso'],
      'sexo': aluno[0]['sexo'],
      'cor_raca': aluno[0]['cor_raca'],
      'idade_ingresso': int(ndado[0][6]),
      'deficiencia': aluno[0]['deficiencia'],
      'media_global_aluno': aluno[0]['media_global_aluno'],
      'media_global_curso': aluno[0]['media_global_curso'],
      'percentual_integralizado': aluno[0]['percentual_integralizado'],
      'escola_publica': aluno[0]['escola_publica'],
      'escola_ensino_medio': aluno[0]['escola_ensino_medio'],
      'cidade_endereco': aluno[0]['cidade_endereco'],
      'uf_endereco': aluno[0]['uf_endereco'],
      'total_trancamentos': aluno[0]['total_trancamentos']
   }

   return result
