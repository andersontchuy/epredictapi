import sqlite3

# Função para inserir um usuário
def data_insert(nome, email, senha):
    conn = sqlite3.connect('./data/users.db') # Criando uma conexão
    c = conn.cursor() # Criando um cursor

    sql_insert = 'insert into user (nome, email, senha) values (?, ?, ?)'
    c.execute(sql_insert, (nome, email, senha))
    conn.commit()
    c.close()
    conn.close()

# Leitura de registros específicos        
def busca_usuario(email, senha):
    conn = sqlite3.connect('./data/users.db') # Criando uma conexão
    c = conn.cursor() # Criando um cursor

    sql_select = 'select nome, email from user where email == ? and senha == ?'
    c.execute(sql_select, (email, senha))
    result = ''
    for registro in c.fetchall():
        result = registro 
    
    c.close() # Fechando cursor
    conn.close() # Fechando conexão
    if result == []:
        return 0
    return result
