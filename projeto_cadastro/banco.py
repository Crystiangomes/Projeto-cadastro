import sqlite3

DB = "biblioteca.db"

def conectar():
    return sqlite3.connect(DB)

# ---------------- TABELAS ----------------
def criar_tabela():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            disponivel TEXT NOT NULL, -- “Sim” ou “Não”
            imagem TEXT -- caminho da capa
        )
    """)
    con.commit()
    con.close()

def criar_tabela_usuarios():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def criar_tabela_emprestimos():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            livro_id INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            dias_restantes INTEGER NOT NULL,
            FOREIGN KEY(livro_id) REFERENCES livros(id)
        )
    """)
    con.commit()
    con.close()

# ---------------- LIVROS ----------------
def inserir(titulo, autor, disponivel, imagem=None):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO livros (titulo, autor, disponivel, imagem) VALUES (?,?,?,?)",
        (titulo, autor, disponivel, imagem)
    )
    con.commit()
    con.close()

def listar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM livros")
    dados = cur.fetchall()
    con.close()
    return dados

def editar(id_livro, titulo, autor, disponivel, imagem=None):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE livros
        SET titulo=?, autor=?, disponivel=?, imagem=?
        WHERE id=?
    """, (titulo, autor, disponivel, imagem, id_livro))
    con.commit()
    con.close()

def excluir(id_livro):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM livros WHERE id=?", (id_livro,))
    con.commit()
    con.close()

# ---------------- USUÁRIOS ----------------
def inserir_usuario(nome, email, senha):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
    con.commit()
    con.close()

def verificar_login(email, senha):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    usuario = cur.fetchone()
    con.close()
    return usuario

# ---------------- EMPRÉSTIMOS ----------------
def emprestar_livro(usuario, livro_id, data, dias):
    con = conectar()
    cur = con.cursor()
    # registra empréstimo
    cur.execute("INSERT INTO emprestimos (usuario, livro_id, data_emprestimo, dias_restantes) VALUES (?, ?, ?, ?)",
                (usuario, livro_id, data, dias))
    # atualiza disponibilidade
    cur.execute("UPDATE livros SET disponivel=? WHERE id=?", ("Não", livro_id))
    con.commit()
    con.close()

def devolver_livro(livro_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE livros SET disponivel=? WHERE id=?", ("Sim", livro_id))
    con.commit()
    con.close()

def listar_emprestimos(usuario):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT livros.titulo, livros.autor, emprestimos.data_emprestimo, emprestimos.dias_restantes
        FROM emprestimos
        JOIN livros ON emprestimos.livro_id = livros.id
        WHERE emprestimos.usuario=?
    """, (usuario,))
    dados = cur.fetchall()
    con.close()
    return dados



# Criar tabelas no início
criar_tabela()
criar_tabela_usuarios()
criar_tabela_emprestimos()


