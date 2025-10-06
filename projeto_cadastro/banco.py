import sqlite3
from datetime import datetime, timedelta

# ====================== CONEXÃO ===========================
def conectar():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    return conexao, cursor


# ====================== CRIAÇÃO DAS TABELAS ===========================
def criar_tabelas():
    conexao, cursor = conectar()

    # Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            curso TEXT,
            cep TEXT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Livros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            disponivel TEXT NOT NULL,
            imagem TEXT,
            pdf_path TEXT
        )
    """)

    # Empréstimos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_email TEXT NOT NULL,
            livro_id INTEGER NOT NULL,
            titulo_livro TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT NOT NULL,
            FOREIGN KEY (livro_id) REFERENCES livros(id),
            FOREIGN KEY (usuario_email) REFERENCES usuarios(email)
        )
    """)

    # Avaliações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            usuario TEXT NOT NULL,
            nota INTEGER NOT NULL CHECK(nota BETWEEN 1 AND 5),
            comentario TEXT,
            FOREIGN KEY (id_livro) REFERENCES livros(id)
        )
    """)

    conexao.commit()
    conexao.close()


# ====================== USUÁRIOS ===========================
def inserir_usuario(nome, idade, curso, cep, email, senha):
    conexao, cursor = conectar()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, idade, curso, cep, email, senha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, idade, curso, cep, email, senha))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Usuário com e-mail {email} já existe.")
        return False
    finally:
        conexao.close()


def verificar_login(email, senha):
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario


def buscar_dados_usuario(email):
    conexao, cursor = conectar()
    cursor.execute("SELECT nome, idade, curso, cep, email FROM usuarios WHERE email = ?", (email,))
    dados = cursor.fetchone()
    conexao.close()
    return dados


def atualizar_dados_usuario(email, nome, idade, curso, cep, senha=None):
    conexao, cursor = conectar()
    try:
        if senha:
            cursor.execute("""
                UPDATE usuarios
                SET nome = ?, idade = ?, curso = ?, cep = ?, senha = ?
                WHERE email = ?
            """, (nome, idade, curso, cep, senha, email))
        else:
            cursor.execute("""
                UPDATE usuarios
                SET nome = ?, idade = ?, curso = ?, cep = ?
                WHERE email = ?
            """, (nome, idade, curso, cep, email))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("❌ Erro ao atualizar usuário:", e)
        return False
    finally:
        conexao.close()


# ====================== LIVROS ===========================
def inserir_livro(titulo, autor, disponivel="Sim", imagem=None, pdf_path=None):
    conexao, cursor = conectar()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, disponivel, imagem, pdf_path)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, autor, disponivel, imagem, pdf_path))
    conexao.commit()
    conexao.close()


def listar_livros():
    conexao, cursor = conectar()
    cursor.execute("SELECT id, titulo, autor, disponivel, imagem, pdf_path FROM livros")
    livros = cursor.fetchall()
    conexao.close()
    return livros


def editar_livro(id_livro, titulo, autor, disponivel, imagem=None, pdf_path=None):
    conexao, cursor = conectar()
    cursor.execute("""
        UPDATE livros
        SET titulo = ?, autor = ?, disponivel = ?, imagem = ?, pdf_path = ?
        WHERE id = ?
    """, (titulo, autor, disponivel, imagem, pdf_path, id_livro))
    conexao.commit()
    conexao.close()


def excluir_livro(id_livro):
    conexao, cursor = conectar()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
    conexao.commit()
    conexao.close()


def atualizar_disponibilidade(id_livro, disponivel):
    conexao, cursor = conectar()
    cursor.execute("UPDATE livros SET disponivel = ? WHERE id = ?", (disponivel, id_livro))
    conexao.commit()
    conexao.close()


def obter_pdf_livro(id_livro):
    conexao, cursor = conectar()
    cursor.execute("SELECT pdf_path FROM livros WHERE id = ?", (id_livro,))
    resultado = cursor.fetchone()
    conexao.close()
    if resultado and resultado[0]:
        return resultado[0]
    return None


def listar_livros_emprestados_usuario(email_usuario):
    conexao, cursor = conectar()
    cursor.execute("""
        SELECT l.id, l.titulo, l.autor, l.pdf_path
        FROM livros l
        INNER JOIN emprestimos e ON l.id = e.livro_id
        WHERE e.usuario_email = ?
    """, (email_usuario,))
    livros = cursor.fetchall()
    conexao.close()
    return livros


# ====================== EMPRÉSTIMOS ===========================
def registrar_emprestimo(usuario_email, id_livro, titulo_livro):
    conexao, cursor = conectar()
    data_emprestimo = datetime.now()
    data_devolucao = data_emprestimo + timedelta(days=30)

    cursor.execute("""
        INSERT INTO emprestimos (usuario_email, livro_id, titulo_livro, data_emprestimo, data_devolucao)
        VALUES (?, ?, ?, ?, ?)
    """, (
        usuario_email,
        id_livro,
        titulo_livro,
        data_emprestimo.strftime("%Y-%m-%d %H:%M:%S"),
        data_devolucao.strftime("%Y-%m-%d %H:%M:%S")
    ))

    cursor.execute("UPDATE livros SET disponivel = 'Não' WHERE id = ?", (id_livro,))
    conexao.commit()
    conexao.close()


def listar_emprestimos_usuario(email_usuario):
    conexao, cursor = conectar()
    cursor.execute("""
        SELECT titulo_livro, data_emprestimo, data_devolucao
        FROM emprestimos
        WHERE usuario_email = ?
    """, (email_usuario,))
    resultados = cursor.fetchall()
    conexao.close()

    emprestimos = []
    for titulo, data_emprestimo, data_devolucao in resultados:
        try:
            data_dev = datetime.strptime(data_devolucao, "%Y-%m-%d %H:%M:%S")
            dias_restantes = (data_dev - datetime.now()).days
        except Exception:
            dias_restantes = "N/A"
        emprestimos.append((titulo, data_emprestimo, data_devolucao, dias_restantes))
    return emprestimos


# ====================== DEVOLUÇÃO ===========================
def devolver_livro(usuario_email, id_livro):
    """Remove o empréstimo e marca o livro como disponível novamente"""
    conexao, cursor = conectar()
    cursor.execute("DELETE FROM emprestimos WHERE usuario_email = ? AND livro_id = ?", (usuario_email, id_livro))
    cursor.execute("UPDATE livros SET disponivel = 'Sim' WHERE id = ?", (id_livro,))
    conexao.commit()
    conexao.close()


# ====================== AVALIAÇÕES ===========================
def registrar_avaliacao(id_livro, usuario, nota, comentario):
    """Registra ou atualiza uma avaliação do usuário para um livro"""
    conexao, cursor = conectar()
    cursor.execute("SELECT id FROM avaliacoes WHERE id_livro = ? AND usuario = ?", (id_livro, usuario))
    existente = cursor.fetchone()

    if existente:
        cursor.execute("""
            UPDATE avaliacoes
            SET nota = ?, comentario = ?
            WHERE id_livro = ? AND usuario = ?
        """, (nota, comentario, id_livro, usuario))
    else:
        cursor.execute("""
            INSERT INTO avaliacoes (id_livro, usuario, nota, comentario)
            VALUES (?, ?, ?, ?)
        """, (id_livro, usuario, nota, comentario))

    conexao.commit()
    conexao.close()


def obter_avaliacoes(id_livro):
    conexao, cursor = conectar()
    cursor.execute("SELECT usuario, nota, comentario FROM avaliacoes WHERE id_livro = ?", (id_livro,))
    avaliacoes = cursor.fetchall()
    conexao.close()
    return avaliacoes


# ====================== EXECUÇÃO AUTOMÁTICA ===========================
if __name__ == "__main__":
    criar_tabelas()
    print("✅ Banco de dados atualizado com suporte a devolução e avaliações de livros.")
