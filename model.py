#coding: utf-8
import pickle
from normalize import normalizaDados

evasion = pickle.load(open('./modelo/evasao_modelo_v3.0.sav','rb'))

def preveEvasao(aluno):
   result = evasion.predict(aluno.reshape(1, -1))
   return result

def calculaProbabilidade(aluno):
   prob = evasion.predict_proba(aluno.reshape(1, -1))
   return prob

def listaAlunoPredito(lista):
   # lista_aluno = []
   # for aluno in range(len(lista)):
   #    predicao = preveEvasao(lista[aluno])
   #    if predicao == 'sim':
   #       lista_aluno.append(lista[aluno])
   lista_aluno = {}
   for aluno in range(len(lista)):
      predicao = preveEvasao(lista[aluno])
      if predicao == 'sim':
         lista_aluno[aluno] = lista[aluno]

   return lista_aluno

def listaAlunoPorCurso(lista, curso):
    lista_aluno = []
    [lista_aluno.append(dado[0]) for dado in lista if dado[0] == curso]
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
   cc, es, si = separaAlunoPorCurso(nlista) # dividindo todos os alunos
   qcc = len(cc)
   qes = len(es)
   qsi = len(si)
   cc, es, si = [], [], []
   cc, es, si = separaAlunoPorCurso(list(alunos.values())) # dividindo alunos preditos
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
      curso = 1
   elif id_curso == 'b' or id_curso == 'es':
      curso = 2
   elif id_curso == 'c' or id_curso == 'si':
      curso = 3
   else:
      return 0
      
   nlista = normalizaDados(lista)
   lista_aluno = listaAlunoPorCurso(nlista, curso)
   lista_evasao = listaAlunoPredito(nlista)
   lista_evasao_curso = listaAlunoPorCurso(list(lista_evasao.values()), curso)
   

   total_aluno = len(lista_aluno)
   total_evasao = len(lista_evasao_curso)
   percentual = int(round((total_evasao/total_aluno) * 100, 2))

   result = {
      'total_aluno': str(total_aluno),
      'total_evasao': str(total_evasao),
      'percentual_evasao': str(percentual),
   }
   return result