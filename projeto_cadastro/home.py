import tkinter as tk
from tkinter import messagebox
import sqlite3

# conexão com banco
def conectar():
    return sqlite3.connect("biblioteca.db")

# função de pesquisa de livros
def pesquisar_livros(criterio, valor):
    con = conectar()
    cur = con.cursor()
    if criterio == "Título":
        cur.execute("SELECT titulo, autor, disponibilidade FROM livros WHERE titulo LIKE ?", ('%' + valor + '%',))
    elif criterio == "Autor":
        cur.execute("SELECT titulo, autor, disponibilidade FROM livros WHERE autor LIKE ?", ('%' + valor + '%',))
    elif criterio == "Disponibilidade":
        cur.execute("SELECT titulo, autor, disponibilidade FROM livros WHERE disponibilidade = ?", (valor,))
    else:
        return []
    resultados = cur.fetchall()
    con.close()
    return resultados

# tela home com Toplevel
def home_page(usuario, master=None):
    # Se já existe uma janela_home principal, abre como Toplevel
    home = tk.Toplevel(master) if master else tk.Tk()
    home.title("Home - Biblioteca")
    home.geometry("800x500")
    home.config(bg="#f5f5f5")

    # ----- MENU LATERAL -----
    menu_lateral = tk.Frame(home, bg="#5a8c89", width=200, height=500)
    menu_lateral.pack(side="left", fill="y")

    tk.Label(menu_lateral, text="📚 BIBLIOTECA", bg="#5a8c89", fg="white",
             font=("Arial", 14, "bold")).pack(pady=20)

    # PERFIL
    def abrir_perfil():
        perfil = tk.Toplevel(home)
        perfil.title("Perfil do Usuário")
        perfil.geometry("400x300")
        perfil.config(bg="white")

        tk.Label(perfil, text="👤 Perfil do Usuário", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # exemplo de dados -> depois pode puxar do BD
        dados_usuario = {
            "Nome": usuario,
            "Email": "usuario@email.com",
            "Data de Cadastro": "01/10/2025",
            "Livros Emprestados": "2"
        }

        for chave, valor in dados_usuario.items():
            tk.Label(perfil, text=f"{chave}: {valor}", font=("Arial", 12), bg="white").pack(anchor="w", padx=20, pady=5)

        tk.Button(perfil, text="Fechar", command=perfil.destroy, bg="#5a8c89", fg="white").pack(pady=15)

    # HISTÓRICO
    def abrir_historico():
        historico_janela = tk.Toplevel(home)
        historico_janela.title("Histórico de Empréstimos")
        historico_janela.geometry("600x400")
        historico_janela.config(bg="white")

        tk.Label(historico_janela, text="📖 Histórico de Empréstimos", font=("Arial", 14, "bold"),
                 bg="white").pack(pady=10)

        con = conectar()
        cur = con.cursor()
        cur.execute("""SELECT livros.titulo, livros.autor, emprestimos.data_emprestimo, emprestimos.dias_restantes
                       FROM emprestimos 
                       JOIN livros ON emprestimos.livro_id = livros.id
                       WHERE emprestimos.usuario = ?""", (usuario,))
        historico = cur.fetchall()
        con.close()

        if historico:
            frame = tk.Frame(historico_janela, bg="white")
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            for h in historico:
                tk.Label(frame, text=f"Livro: {h[0]} | Autor: {h[1]} | Data: {h[2]} | Dias Restantes: {h[3]}",
                         font=("Arial", 11), bg="white", anchor="w", justify="left", wraplength=550).pack(anchor="w", pady=5)
        else:
            tk.Label(historico_janela, text="Nenhum livro emprestado ainda.", font=("Arial", 12), bg="white").pack(pady=20)

        tk.Button(historico_janela, text="Fechar", command=historico_janela.destroy, bg="#5a8c89", fg="white").pack(pady=15)

    # PESQUISA
    def abrir_pesquisa():
        pesquisa_janela = tk.Toplevel(home)
        pesquisa_janela.title("Pesquisar Livros")
        pesquisa_janela.geometry("400x300")

        tk.Label(pesquisa_janela, text="Pesquisar por:").pack(pady=5)
        criterio_var = tk.StringVar(value="Título")
        criterios = ["Título", "Autor", "Disponibilidade"]
        criterio_menu = tk.OptionMenu(pesquisa_janela, criterio_var, *criterios)
        criterio_menu.pack()

        tk.Label(pesquisa_janela, text="Valor:").pack(pady=5)
        valor_entry = tk.Entry(pesquisa_janela)
        valor_entry.pack(pady=5)

        def executar_pesquisa():
            valor = valor_entry.get()
            resultados = pesquisar_livros(criterio_var.get(), valor)
            if resultados:
                res_texto = "\n".join([f"Título: {r[0]}, Autor: {r[1]}, Disp: {r[2]}" for r in resultados])
                messagebox.showinfo("Resultados", res_texto)
            else:
                messagebox.showinfo("Resultados", "Nenhum livro encontrado.")

        tk.Button(pesquisa_janela, text="Pesquisar", command=executar_pesquisa).pack(pady=10)

    def sair():
        home.destroy()

    # botões no menu lateral
    botoes_menu = [
        ("👤 Perfil", abrir_perfil),
        ("📖 Histórico", abrir_historico),
        ("🔍 Pesquisar Livros", abrir_pesquisa),
        ("🚪 Sair", sair),
    ]

    for texto, comando in botoes_menu:
        tk.Button(menu_lateral, text=texto, command=comando, width=20, bg="#5a8c89",
                  fg="white", relief="flat", font=("Arial", 11)).pack(pady=10)

    # ----- CONTEÚDO PRINCIPAL -----
    conteudo = tk.Frame(home, bg="white", width=600, height=500, relief="solid", bd=1)
    conteudo.pack(side="right", fill="both", expand=True)

    tk.Label(conteudo, text=f"Bem-vindo, {usuario}!", font=("Arial", 16, "bold"),
             bg="white").pack(pady=40)

    tk.Label(conteudo, text="Aqui você pode acessar seu perfil, ver seu histórico e pesquisar livros.",
             font=("Arial", 12), bg="white").pack(pady=10)

    # só roda o loop se for janela_home principal
    if master is None:
        home.mainloop()

if __name__ == "__main__":
    # substitua "UsuárioTeste" pelo nome do usuário logado que você quiser
    home_page("UsuárioTeste")
