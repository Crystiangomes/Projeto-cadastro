import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
from banco import (
    listar_livros,
    registrar_emprestimo,
    listar_emprestimos_usuario,
    listar_livros_emprestados_usuario,
    buscar_dados_usuario,
    atualizar_dados_usuario,
    devolver_livro,
    registrar_avaliacao,
)
import leitura  # integração com a página de leitura


def home_page(root, usuario_email):
    """Tela principal do sistema da biblioteca"""
    # ====== LIMPAR TELA ANTERIOR ======
    for widget in root.winfo_children():
        widget.destroy()
    root.update_idletasks()

    root.title("Biblioteca - Página Inicial")
    root.geometry("950x600")
    root.configure(bg="#F8F9FA")
    root.state("zoomed")

    # ====== FRAME PRINCIPAL ======
    frame_principal = tk.Frame(root, bg="#F8F9FA")
    frame_principal.pack(fill="both", expand=True)

    # ====== MENU LATERAL ======
    menu_lateral = tk.Frame(frame_principal, bg="#4D908E", width=200)
    menu_lateral.pack(side="left", fill="y")

    # ====== CONTEÚDO PRINCIPAL ======
    conteudo = tk.Frame(frame_principal, bg="#F8F9FA")
    conteudo.pack(side="right", expand=True, fill="both")

    def limpar_conteudo():
        for widget in conteudo.winfo_children():
            widget.destroy()
        root.update_idletasks()

    # ====== INÍCIO ======
    def mostrar_inicio():
        limpar_conteudo()
        tk.Label(
            conteudo,
            text="🏠 Bem-vindo à Biblioteca",
            font=("Arial", 22, "bold"),
            bg="#F8F9FA"
        ).pack(pady=20)

        tk.Label(
            conteudo,
            text=f"Usuário logado: {usuario_email}",
            bg="#F8F9FA",
            font=("Arial", 13)
        ).pack(pady=10)

        # ====== TEXTO BIBLIOTECA ======
        texto_biblioteca = (
            "Nossa biblioteca foi criada com o objetivo de incentivar a leitura e facilitar o acesso a livros digitais.\n"
            "Aqui, você pode explorar diferentes gêneros, descobrir novos autores e gerenciar sua coleção pessoal com facilidade.\n\n"
            "Nosso objetivo é tornar a leitura acessível, agradável e sempre ao seu alcance.\n"
            "Você pode organizar seus livros, acompanhar suas leituras e conhecer novos autores, tudo em um só lugar."
        )

        tk.Label(
            conteudo,
            text=texto_biblioteca,
            wraplength=800,
            justify="left",
            bg="#F8F9FA",
            font=("Arial", 13),
            fg="#000000"
        ).pack(pady=40)

    # ====== LIVROS DISPONÍVEIS ======
    def mostrar_livros():
        limpar_conteudo()
        tk.Label(conteudo, text="📚 Livros Disponíveis", bg="#F8F9FA", font=("Arial", 18, "bold")).pack(pady=10)

        livros = listar_livros()
        if not livros:
            tk.Label(conteudo, text="Nenhum livro cadastrado no momento.", bg="#F8F9FA").pack(pady=20)
            return

        lista_frame = tk.Frame(conteudo, bg="#F8F9FA")
        lista_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(lista_frame, bg="#F8F9FA", highlightthickness=0)
        scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F8F9FA")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        emprestados = [livro[0] for livro in listar_livros_emprestados_usuario(usuario_email)]

        for id_livro, titulo, autor, disponivel, imagem, pdf_path in livros:
            card = tk.Frame(scroll_frame, bg="#FFFFFF", relief="solid", bd=1)
            card.pack(pady=5, padx=15, fill="x")

            # Capa
            if imagem and os.path.exists(imagem):
                try:
                    img = Image.open(imagem).resize((70, 100))
                    capa = ImageTk.PhotoImage(img)
                except Exception:
                    capa = ImageTk.PhotoImage(Image.new("RGB", (70, 100), "#ccc"))
            else:
                capa = ImageTk.PhotoImage(Image.new("RGB", (70, 100), "#ccc"))

            lbl_capa = tk.Label(card, image=capa, bg="#FFFFFF")
            lbl_capa.image = capa
            lbl_capa.pack(side="left", padx=10, pady=10)

            info = tk.Frame(card, bg="#FFFFFF")
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=titulo, font=("Arial", 14, "bold"), bg="#FFFFFF").pack(anchor="w")
            tk.Label(info, text=f"Autor: {autor}", bg="#FFFFFF").pack(anchor="w")

            botoes_frame = tk.Frame(card, bg="#FFFFFF")
            botoes_frame.pack(side="right", padx=10, pady=10)

            if id_livro in emprestados:
                tk.Button(
                    botoes_frame,
                    text="📖 Ler",
                    bg="#2A9D8F",
                    fg="white",
                    cursor="hand2",
                    command=lambda id_l=id_livro, t=titulo: abrir_leitura(id_l, t)
                ).pack(pady=3)
                tk.Button(
                    botoes_frame,
                    text="⭐ Avaliar",
                    bg="#F4A261",
                    fg="white",
                    cursor="hand2",
                    command=lambda id_l=id_livro, t=titulo: avaliar(id_l, t)
                ).pack(pady=3)
                tk.Button(
                    botoes_frame,
                    text="↩️ Devolver",
                    bg="#E76F51",
                    fg="white",
                    cursor="hand2",
                    command=lambda id_l=id_livro, t=titulo: devolver(id_l, t)
                ).pack(pady=3)
            elif disponivel.lower() == "sim":
                tk.Button(
                    botoes_frame,
                    text="📘 Pegar emprestado",
                    bg="#4D908E",
                    fg="white",
                    cursor="hand2",
                    command=lambda id_l=id_livro, t=titulo: emprestar_livro(id_l, t)
                ).pack(pady=3)
            else:
                tk.Label(card, text="Indisponível", fg="red", bg="#FFFFFF", font=("Arial", 10, "bold")).pack(side="bottom", pady=5)

    # ====== LEITURA ======
    def abrir_leitura(id_livro, titulo):
        for widget in root.winfo_children():
            widget.destroy()
        root.update_idletasks()
        leitura.leitura_page(root, usuario_email, id_livro, titulo)

    # ====== LEITURA PESSOAL ======
    def mostrar_leitura():
        limpar_conteudo()
        tk.Label(conteudo, text="📖 Seus Livros para Leitura", bg="#F8F9FA", font=("Arial", 18, "bold")).pack(pady=10)

        livros_emprestados = listar_livros_emprestados_usuario(usuario_email)
        if not livros_emprestados:
            tk.Label(conteudo, text="Você não possui livros emprestados no momento.", bg="#F8F9FA").pack(pady=20)
            return

        for id_livro, titulo, autor, pdf_path in livros_emprestados:
            card = tk.Frame(conteudo, bg="#FFFFFF", relief="solid", bd=1)
            card.pack(pady=5, padx=15, fill="x")

            tk.Label(card, text=titulo, font=("Arial", 14, "bold"), bg="#FFFFFF").pack(anchor="w", padx=10, pady=5)
            tk.Label(card, text=f"Autor: {autor}", bg="#FFFFFF").pack(anchor="w", padx=10)

            botoes = tk.Frame(card, bg="#FFFFFF")
            botoes.pack(anchor="e", padx=10, pady=5)

            tk.Button(botoes, text="📖 Ler", bg="#4D908E", fg="white",
                      command=lambda id=id_livro, t=titulo: abrir_leitura(id, t)).pack(side="left", padx=5)
            tk.Button(botoes, text="⭐ Avaliar", bg="#F4A261", fg="white",
                      command=lambda id=id_livro, t=titulo: avaliar(id, t)).pack(side="left", padx=5)
            tk.Button(botoes, text="↩️ Devolver", bg="#E76F51", fg="white",
                      command=lambda id=id_livro, t=titulo: devolver(id, t)).pack(side="left", padx=5)

    # ====== DEVOLVER LIVRO ======
    def devolver(id_livro, titulo):
        if messagebox.askyesno("Confirmação", f"Deseja devolver o livro '{titulo}'?"):
            try:
                devolver_livro(usuario_email, id_livro)
                messagebox.showinfo("Sucesso", f"'{titulo}' foi devolvido com sucesso!")
                mostrar_livros()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao devolver o livro:\n{e}")

    # ====== AVALIAR LIVRO ======
    def avaliar(id_livro, titulo):
        nota = simpledialog.askinteger("Avaliação", f"Dê uma nota de 1 a 5 para '{titulo}':", minvalue=1, maxvalue=5)
        if nota:
            comentario = simpledialog.askstring("Comentário", f"Quer deixar um comentário sobre '{titulo}'?")
            try:
                registrar_avaliacao(id_livro, usuario_email, nota, comentario or "")
                messagebox.showinfo("Obrigado!", f"Você avaliou '{titulo}' com {nota} estrela(s)!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao registrar avaliação:\n{e}")

    # ====== HISTÓRICO ======
    def mostrar_historico():
        limpar_conteudo()
        tk.Label(conteudo, text="📜 Histórico de Empréstimos", bg="#F8F9FA", font=("Arial", 18, "bold")).pack(pady=10)
        emprestimos = listar_emprestimos_usuario(usuario_email)
        if not emprestimos:
            tk.Label(conteudo, text="Nenhum empréstimo registrado.", bg="#F8F9FA").pack(pady=20)
            return
        for titulo, data_emp, data_dev, dias_rest in emprestimos:
            frame = tk.Frame(conteudo, bg="#FFFFFF", relief="solid", bd=1)
            frame.pack(pady=5, padx=20, fill="x")
            texto = f"Título: {titulo}\nData de Empréstimo: {data_emp}\nData de Devolução: {data_dev}\nDias Restantes: {dias_rest} dias"
            tk.Label(frame, text=texto, bg="#FFFFFF", anchor="w", justify="left").pack(side="left", padx=10, pady=5)

    # ====== PERFIL ======
    def mostrar_perfil():
        limpar_conteudo()
        tk.Label(conteudo, text="👤 Perfil do Usuário", bg="#F8F9FA", font=("Arial", 18, "bold")).pack(pady=10)
        dados = buscar_dados_usuario(usuario_email)
        if not dados:
            tk.Label(conteudo, text="Erro ao carregar dados do usuário.", bg="#F8F9FA", fg="red").pack(pady=20)
            return
        nome, idade, curso, cep, email = dados
        campos = {
            "Nome": tk.StringVar(value=nome),
            "Idade": tk.StringVar(value=str(idade) if idade else ""),
            "Curso": tk.StringVar(value=curso if curso else ""),
            "CEP": tk.StringVar(value=cep if cep else ""),
            "Senha (nova)": tk.StringVar()
        }
        for label, var in campos.items():
            tk.Label(conteudo, text=label + ":", bg="#F8F9FA", anchor="w").pack(pady=3)
            tk.Entry(conteudo, textvariable=var, width=40, show="*" if "Senha" in label else "").pack(pady=2)
        def salvar():
            sucesso = atualizar_dados_usuario(
                email=usuario_email,
                nome=campos["Nome"].get(),
                idade=int(campos["Idade"].get()) if campos["Idade"].get().isdigit() else None,
                curso=campos["Curso"].get(),
                cep=campos["CEP"].get(),
                senha=campos["Senha (nova)"].get() or None
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar os dados.")
        tk.Button(conteudo, text="💾 Salvar Alterações", bg="#4D908E", fg="white", command=salvar).pack(pady=15)

    # ====== SAIR ======
    def sair():
        for widget in root.winfo_children():
            widget.destroy()
        import login
        login.abrir_login()

    # ====== MENU ======
    botoes = [
        ("🏠 Início", mostrar_inicio),
        ("📚 Livros", mostrar_livros),
        ("📖 Leitura", mostrar_leitura),
        ("📜 Histórico", mostrar_historico),
        ("👤 Perfil", mostrar_perfil),
        ("🚪 Sair", sair),
    ]
    for texto, comando in botoes:
        tk.Button(
            menu_lateral,
            text=texto,
            bg="#4D908E",
            fg="white",
            relief="flat",
            anchor="w",
            cursor="hand2",
            command=comando
        ).pack(fill="x", padx=10, pady=5)

    # ====== EMPRÉSTIMO ======
    def emprestar_livro(id_livro, titulo):
        try:
            registrar_emprestimo(usuario_email, id_livro, titulo)
            messagebox.showinfo("Sucesso", f"Você pegou '{titulo}' emprestado!")
            mostrar_livros()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao registrar o empréstimo:\n{e}")

    mostrar_inicio()
