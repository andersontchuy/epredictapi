#coding: utf-8
import pandas as pd
import json

def normalizaDados(dado):
    df = pd.read_json(json.dumps(dado), orient='list')
    
    # Removendo colunas com informações sem relevância para predição
    df.drop(
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
    df['curso'] = df['curso'].map(curso_map)

    # discretizando variável turno
    turno_map = {'Integral': 0, 'Noturno': 1}
    df['turno'] = df['turno'].map(turno_map)
    df['turno'] = df['turno'].astype('float64')

    # discretizando variável forma de ingresso
    forma_ingresso_map = {
        'INGRESSO POR PROCESSO SELETIVO DECISÃO JUDICIAL': 0, 'INGRESSO POR TRANSFERÊNCIA': 1, 
        'INGRESSO POR TRANSFERÊNCIA EX-OFFICIO': 2, 'INGRESSO PORTADOR DE DIPLOMA': 3,
        'INGRESSO PROCESSO SELETIVO': 4, 'PROGRAMA DE INTERCÂMBIO ACADÊMICO INTERNACIONAL': 5,
        'PROGRAMA DE MOBILIDADE ESTUDANTIL': 6, 'SISTEMA DE SELEÇÃO UNIFICADA - SiSU': 7,
        'SISTEMA DE SELEÇÃO UNIFICADA DECISÃO JUDICIAL': 8, 'SISU COTA': 9
    }
    df['forma_ingresso'] = df['forma_ingresso'].map(forma_ingresso_map)
    df['forma_ingresso'] = df['forma_ingresso'].astype('float64')

    # discretizando variável especificidade de ingresso
    especificidade_ingresso_map = {
        'PREENCHIMENTO DE VAGAS REMANESCENTES': 1, 'UFGINCLUI': 2
    }
    df['especificidade_ingresso'] = df['especificidade_ingresso'].map(
        especificidade_ingresso_map)
    df.loc[df['especificidade_ingresso'].isnull(), 'especificidade_ingresso'] = 0
    df['especificidade_ingresso'] = df['especificidade_ingresso'].astype('float64')

    # discretizando variável categoria de ingresso
    categoria_ingresso_map = {
        'TRANSFERÊNCIA FACULTATIVA': 1, 'INDÍGENA': 2, 'MUDANÇA DE CURSO': 3,
        'PORTADOR DE DIPLOMA': 4, 'QUILOMBOLA': 5
    }
    df['categoria_ingresso'] = df['categoria_ingresso'].map(categoria_ingresso_map)
    df.loc[df['categoria_ingresso']. isnull(), 'categoria_ingresso'] = 0

    # discretizando variável cor/raça
    cor_raca_map = {
        'Não informado': 0, 'Não quis declarar cor/raça': 0, 'Amarelo': 1,
        'Branco': 2, 'Indígeno': 3, 'Pardo': 4, 'Preto': 5
    }
    df['cor_raca'] = df['cor_raca'].map(cor_raca_map)
    df.loc[df['cor_raca'].isnull(), 'cor_raca'] = 0
    df['cor_raca'] = df['cor_raca'].astype('float64')

    # discretizando variável deficiência
    deficiencia_map = {
        'Física': 1, 'Visual': 1, 'Baixa Visão': 1, 'Autismo': 1, 'Auditiva': 1
    }
    df['deficiencia'] = df['deficiencia'].map(deficiencia_map)
    df.loc[df['deficiencia'].isnull(), 'deficiencia'] = 0
    df['deficiencia'] = df['deficiencia'].astype('float64')

    # discretizando variável escola pública
    escola_publica_map = {'NÃO': 0, 'SIM': 1}
    df['escola_publica'] = df['escola_publica'].map(escola_publica_map)
    df.loc[df['escola_publica'].isnull(), 'escola_publica'] = 2
    df['escola_publica'] = df['escola_publica'].astype('float64')

    # discretizando variável sexo
    sexo_map = {'MASCULINO': 0, 'FEMININO': 1}
    df['sexo'] = df['sexo'].map(sexo_map)
    df['sexo'] = df['sexo'].astype('float64')

    # discretizando variável semestre ingresso
    df['semestre_ingresso'] = df['semestre_ingresso'].transform(lambda x: x * 0.1)
    df['ano_periodo_ingresso'] = df['ano_ingresso'] + df['semestre_ingresso']
    df.drop(['ano_ingresso', 'semestre_ingresso'], inplace=True, axis=1)

    # criando variável idade ingresso 
    ano_nascimento = df['dt_nascimento'].str[6:].astype('float64')
    ano_ingresso = round(df['ano_periodo_ingresso'])
    df['idade_ingresso'] = ano_ingresso - ano_nascimento
    df.drop(['dt_nascimento'], inplace=True, axis=1)

    # discretizando variável status
    status_map = {
        'ATIVO': 'nao', 'GRADUADO': 'nao', 'ATIVO - FORMANDO': 'nao', 
        'INTEGRALIZADO': 'nao', 'TRANCADO': 'sim', 'EXCLUÍDO': 'sim' 
    }
    df['status'] = df['status'].map(status_map)
    df.loc[df['status'].isnull(), 'status'] = 'sim'

    # criando lista de atributos
    atributos_evasao = [
        'curso', 'turno', 'forma_ingresso', 'especificidade_ingresso', 
        'categoria_ingresso', 'ano_periodo_ingresso', 'idade_ingresso', 'cor_raca',  
        'sexo', 'deficiencia', 'escola_publica', 'media_global_aluno', 
        'media_global_curso', 'percentual_integralizado'
    ]

    result = df[atributos_evasao].values

    return result