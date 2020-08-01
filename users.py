import sqlite3

def abre_conexao():
    # Criando uma conexão
    conn = sqlite3.connect('./data/users.db')
    # Criando um cursor
    c = conn.cursor()
    return conn, c

def fecha_conexao(conn, c):
    c.close()
    conn.close()
    return

# Função para inserir um usuário
def insere_usuario(nome, email, senha):
    conn, c = abre_conexao()
    sql_insert = 'insert into user (nome, email, senha) values (?, ?, ?)'
    c.execute(sql_insert, (nome, email, senha))
    conn.commit()
    fecha_conexao(conn,c)
    return

# Busca usuário por email e senha       
def busca_usuario(email, senha):
    conn, c = abre_conexao()
    sql_select = 'select nome, email, senha from user where email == ? and senha == ?'
    c.execute(sql_select, (email, senha))
    result = ''
    for registro in c.fetchall():
        result = registro 
    fecha_conexao(conn,c)
    if not result:
        return None
    return {"nome": result[0], "email": result[1], "senha": result[2]}

# Busca usuário por email
def usuario_por_email(email):
    conn, c = abre_conexao()
    sql_select = 'select nome, email, senha from user where email == ?'
    c.execute(sql_select, (email,))
    result = ''
    for registro in c.fetchall():
        result = registro 
    fecha_conexao(conn,c)
    if not result:
        return None
    return {"nome": result[0], "email": result[1], "senha": result[2]}

def checa_senha(senha_usuario, senha_autenticacao):
    if senha_usuario == senha_autenticacao:
        return True
    return False 

