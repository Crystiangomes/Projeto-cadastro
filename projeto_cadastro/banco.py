import sqlite3

# ==================================================
# CONEXÃO COM O BANCO DE DADOS
# ==================================================
def conectar():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    return conexao, cursor

# ==================================================
# CRIAÇÃO DAS TABELAS (USUÁRIOS E LIVROS)
# ==================================================
def criar_tabela():
    conexao, cursor = conectar()

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade TEXT,
            curso TEXT,
            cep TEXT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de livros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            disponivel TEXT NOT NULL,
            imagem TEXT
        )
    ''')

    conexao.commit()
    conexao.close()

# ==================================================
# FUNÇÕES PARA USUÁRIOS (CADASTRO E LOGIN)
# ==================================================
def inserir_usuario(nome, idade, curso, cep, email, senha):
    conexao, cursor = conectar()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, idade, curso, cep, email, senha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, idade, curso, cep, email, senha))
        conexao.commit()
        resultado = True
    except sqlite3.IntegrityError:
        resultado = False
    conexao.close()
    return resultado

def verificar_login(email, senha):
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario

# ==================================================
# FUNÇÕES PARA LIVROS (CADASTRO, LISTAGEM, EDIÇÃO, EXCLUSÃO)
# ==================================================
def inserir_livro(titulo, autor, disponivel, imagem):
    conexao, cursor = conectar()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, disponivel, imagem)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, disponivel, imagem))
    conexao.commit()
    conexao.close()

def listar_livros():
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM livros")
    dados = cursor.fetchall()
    conexao.close()
    return dados

def editar_livro(id_livro, titulo, autor, disponivel, imagem):
    conexao, cursor = conectar()
    cursor.execute("""
        UPDATE livros
        SET titulo = ?, autor = ?, disponivel = ?, imagem = ?
        WHERE id = ?
    """, (titulo, autor, disponivel, imagem, id_livro))
    conexao.commit()
    conexao.close()

def excluir_livro(id_livro):
    conexao, cursor = conectar()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
    conexao.commit()
    conexao.close()
