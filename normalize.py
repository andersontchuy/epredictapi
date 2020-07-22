#coding: utf-8
import pandas as pd
import json
from unidecode import unidecode

def normalizaDados(dado):
    df_ies = pd.read_json(json.dumps(dado), orient='list')
    
    # Removendo colunas com informações sem relevância para predição
    df_ies.drop(
        [
            'acao_afirmativa_graduacao','grau_academico', 'modalidade', 'nome_campus',
            'municipio', 'possui_matricula_em_estagio_20182', 'percentual_integralizado_pcc', 
            'acao_afirmativa_participacao_sisu','acao_afirmativa_aprovacao_sisu',
            'possui_matricula_em_disciplina_20182', 'conclusao_ensino_medio',
            'escola_ensino_medio', 'cidade_ensino_medio', 'uf_ensino_medio',
            'cidade_endereco', 'uf_endereco', 'total_trancamentos','unidade',
            'possui_tracamento_compulsorio', 'percentual_integralizado__1',
            'percentual_integralizado_nc', 'percentual_integralizado_ne_obr',
            'percentual_integralizado_ne_opt', 'percentual_integralizado_nl',
            'percentual_integralizado_atv_compl', 'nascimento', 'matricula',
            'id_discente_graduacao', 'matricula_sag', 'codigo_inep', 'sigla_matriz'
        ], inplace=True, axis=1
    )

    # discretizando variável curso
    curso_map = {
        'CIÊNCIA DA COMPUTAÇÃO': 1, 
        'ENGENHARIA DE SOFTWARE': 2, 
        'SISTEMAS DE INFORMAÇÃO': 3
    }
    df_ies['curso'] = df_ies['curso'].map(curso_map)

    # discretizando variável turno
    turno_map = {'Integral': 0, 'Noturno': 1}
    df_ies['turno'] = df_ies['turno'].map(turno_map)
    df_ies['turno'] = df_ies['turno'].astype('float64')

    # discretizando variável forma de ingresso
    forma_ingresso_map = {
        'INGRESSO POR PROCESSO SELETIVO DECISÃO JUDICIAL': 0, 'INGRESSO POR TRANSFERÊNCIA': 1, 
        'INGRESSO POR TRANSFERÊNCIA EX-OFFICIO': 2, 'INGRESSO PORTADOR DE DIPLOMA': 3,
        'INGRESSO PROCESSO SELETIVO': 4, 'PROGRAMA DE INTERCÂMBIO ACADÊMICO INTERNACIONAL': 5,
        'PROGRAMA DE MOBILIDADE ESTUDANTIL': 6, 'SISTEMA DE SELEÇÃO UNIFICADA - SiSU': 7,
        'SISTEMA DE SELEÇÃO UNIFICADA DECISÃO JUDICIAL': 8, 'SISU COTA': 9
    }
    df_ies['forma_ingresso'] = df_ies['forma_ingresso'].map(forma_ingresso_map)
    df_ies['forma_ingresso'] = df_ies['forma_ingresso'].astype('float64')

    # discretizando variável especificidade de ingresso
    especificidade_ingresso_map = {
        'PREENCHIMENTO DE VAGAS REMANESCENTES': 1, 'UFGINCLUI': 2
    }
    df_ies['especificidade_ingresso'] = df_ies['especificidade_ingresso'].map(
        especificidade_ingresso_map)
    df_ies.loc[df_ies['especificidade_ingresso'].isnull(), 'especificidade_ingresso'] = 0
    df_ies['especificidade_ingresso'] = df_ies['especificidade_ingresso'].astype('float64')

    # discretizando variável categoria de ingresso
    categoria_ingresso_map = {
        'TRANSFERÊNCIA FACULTATIVA': 1, 'INDÍGENA': 2, 'MUDANÇA DE CURSO': 3,
        'PORTADOR DE DIPLOMA': 4, 'QUILOMBOLA': 5
    }
    df_ies['categoria_ingresso'] = df_ies['categoria_ingresso'].map(categoria_ingresso_map)
    df_ies.loc[df_ies['categoria_ingresso']. isnull(), 'categoria_ingresso'] = 0

    # discretizando variável cor/raça
    cor_raca_map = {
        'Não informado': 0, 'Não quis declarar cor/raça': 0, 'Amarelo': 1,
        'Branco': 2, 'Indígeno': 3, 'Pardo': 4, 'Preto': 5
    }
    df_ies['cor_raca'] = df_ies['cor_raca'].map(cor_raca_map)
    df_ies.loc[df_ies['cor_raca'].isnull(), 'cor_raca'] = 0
    df_ies['cor_raca'] = df_ies['cor_raca'].astype('float64')

    # discretizando variável deficiência
    deficiencia_map = {
        'Física': 1, 'Visual': 1, 'Baixa Visão': 1, 'Autismo': 1, 'Auditiva': 1
    }
    df_ies['deficiencia'] = df_ies['deficiencia'].map(deficiencia_map)
    df_ies.loc[df_ies['deficiencia'].isnull(), 'deficiencia'] = 0
    df_ies['deficiencia'] = df_ies['deficiencia'].astype('float64')

    # discretizando variável escola pública
    escola_publica_map = {'NÃO': 0, 'SIM': 1}
    df_ies['escola_publica'] = df_ies['escola_publica'].map(escola_publica_map)
    df_ies.loc[df_ies['escola_publica'].isnull(), 'escola_publica'] = 2
    df_ies['escola_publica'] = df_ies['escola_publica'].astype('float64')

    # discretizando variável sexo
    sexo_map = {'MASCULINO': 0, 'FEMININO': 1}
    df_ies['sexo'] = df_ies['sexo'].map(sexo_map)
    df_ies['sexo'] = df_ies['sexo'].astype('float64')

    # discretizando variável semestre ingresso
    df_ies['semestre_ingresso'] = df_ies['semestre_ingresso'].transform(lambda x: x * 0.1)
    df_ies['ano_periodo_ingresso'] = df_ies['ano_ingresso'] + df_ies['semestre_ingresso']
    df_ies.drop(['ano_ingresso', 'semestre_ingresso'], inplace=True, axis=1)

    # criando variável idade ingresso 
    ano_nascimento = df_ies['dt_nascimento'].str[6:].astype('float64')
    ano_ingresso = round(df_ies['ano_periodo_ingresso'])
    df_ies['idade_ingresso'] = ano_ingresso - ano_nascimento
    df_ies.drop(['dt_nascimento'], inplace=True, axis=1)

    # discretizando variável status
    status_map = {
        'ATIVO': 'nao', 'GRADUADO': 'nao', 'ATIVO - FORMANDO': 'nao', 
        'INTEGRALIZADO': 'nao', 'TRANCADO': 'sim', 'EXCLUÍDO': 'sim' 
    }
    df_ies['status'] = df_ies['status'].map(status_map)
    df_ies.loc[df_ies['status'].isnull(), 'status'] = 'sim'

    # criando lista de atributos
    atributos_evasao = [
        'curso', 'turno', 'forma_ingresso', 'especificidade_ingresso', 
        'categoria_ingresso', 'ano_periodo_ingresso', 'idade_ingresso', 'cor_raca',  
        'sexo', 'deficiencia', 'escola_publica', 'media_global_aluno', 
        'media_global_curso', 'percentual_integralizado'
    ]

    result = df_ies[atributos_evasao].values

    return result

df_ideb = pd.read_csv('./data/ideb_ensino_medio-escolas-2017.csv', sep=";")

def normalizaNomeEscola(escola_nome):
    escola_map = {
        'IFG - CAMPUS INHUMAS': [
            'INST.FED. DE EDUC.CIENC.E TECN.DE GOIÁS - INHUMAS',
            'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE GOIÁS - INHUMAS',
            'INSTITUTO FEDERAL DE GOIÁS - INHUMAS'],
        'IFG - CAMPUS GOIANIA': [
            'ESCOLA TECNICA FEDERAL DE GOIAS - CEFET'],
        'IFG - CAMPUS GOIANIA OESTE': [
            'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE GOIÁS'],
        'IFG - CAMPUS URUACU': [
            'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE GOIÁS - URUAÇU'],
        'IFMT - CAMPUS RONDONOPOLIS': [
            'IFMT CAMPUS RONDONÓPOLIS'],
        'CEM ELEFANTE BRANCO': [
            'COLÉGIO CENTRO DE ENSINO MÉDIO ELEFANTE BRANCO'],
        'CENTRO DE ENSINO NASCIMENTO DE MORAES': [
            'CENTRO DE ENSINO \"NASCIMENTO DE MORAES"'],
        'COLEGIO DA POLICIA MILITAR DE GOIAS UNIDADE AYRTON SENNA': [
            'CPMG - Ayrton Senna'],
        'COLEGIO DA POLICIA MILITAR DE GOIAS UNIDADE POLIVALENTE MODELO VASCO DOS REIS': [
            'CPMG - UNID POLIV MODELO VASCO DOS REIS', 
            'CPMG- POLIVALENTE MODELO VASCO DOS REIS', 
            'CPMG - POLIVELENTE MODELO VASCO DOS REIS', 
            'COLÉGIO ESTADUAL DA POLÍCIA MILITAR - UNIDADE POLIVALENTE MODELO VASCO DOS REIS'],
        'COLEGIO DA POLICIA MILITAR UNIDADE COLINA AZUL': [
            'COLÉGIO EST COLINA AZUL'],
        'COLEGIO ESTADUAL ANTONIO OLIVEIRA DA SILVA': [
            'COLÉGIO EST ANTÔNIO OLIVEIRA DA SILVA'],
        'COLEGIO ESTADUAL DOUTOR NEGREIROS': [
            'Colégio Estadual Dr. Negreiros'],
        'COLEGIO ESTADUAL POLIVALENTE DE PALMEIRAS DE GOIAS': [
            'COLÉGIO EST DE PALMEIRAS DE GOIÁS'],
        'COLEGIO ESTADUAL SENADOR TEOTONIO VILELA': [
            'COLEGIO ESTADUAL SEN TEOTONIO VILELA'],
        'COLEGIO INTERATIVA LTDA': [
            'COLÉGIO INTERATIVA'],
        'COLEGIO JAO LTDA': [
            'COLÉGIO INTEGRADO JAÓ', 
            'COLÉGIO INTEGRADO JAO',
            'Colégio Integrado Jaó'],
        'UNID ESC HERMINIO BARREIRA': [
            'UNIDADE ESCOLAR HERMÍNIO BARREIRA']
    }

    for nome_padrao, nomes in escola_map.items():
        for nome in nomes:
            if nome == escola_nome:
                escola_nome = nome_padrao
    return unidecode(escola_nome.upper())
    



