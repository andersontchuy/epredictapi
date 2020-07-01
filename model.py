#coding: utf-8
import pickle
import normalize

def preveEvasao(aluno):
   evasion = pickle.load(open('./modelo/evasao_modelo_v3.0.sav','rb'))
   result = evasion.predict(aluno.reshape(1, -1))
   return result

def mostraPredicaoGeral(dados):
   alunos = []
   for aluno in range(len(dados)):
      predicao = preveEvasao(dados[aluno])
      if predicao == 'sim':
         alunos.append(dados[aluno])
   cc, es, si = [], [], []
   cursos = lambda x: cc.append(dados[0]) if x == 1 else (
      es.append(dados[0]) if x == 2 else si.append(dados[0]))
   for curso in dados:
      cursos(curso[0])
   qcc = len(cc)
   qes = len(es)
   qsi = len(si)
   cc, es, si = [], [], []
   evasao = lambda x: cc.append(alunos[0]) if x == 1 else (
      es.append(alunos[0]) if x == 2 else si.append(alunos[0]))
   for curso in alunos:
      evasao(curso[0])
   qecc = len(cc)
   qees = len(es)
   qesi = len(si)
   qat = len(dados)
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
      'percent_evasao_cc': str(round((qecc/qet) * 100, 2)),
      'percent_evasao_es': str(round((qees/qet) * 100, 2)),
      'percent_evasao_si': str(round((qesi/qet) * 100, 2)),
      'percent_evasao_total': str(round((qet/qat)*100, 2))
      }
   return result

