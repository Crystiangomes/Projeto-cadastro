import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil
from banco import inserir_livro, listar_livros, editar_livro, excluir_livro
from leitura import leitura_page
from home import home_page

def main_page(usuario_email, master=None):
    """Tela administrativa para gerenciar livros da biblioteca."""
    main = tk.Toplevel(master) if master else tk.Tk()
    main.title("Gerenciamento de Livros - Biblioteca")
    main.geometry("950x600")
    main.configure(bg="#f5f5f5")
    main.state("zoomed")

    pasta_imagens = "imagens_livros"
    pasta_pdfs = "pdf_livros"
    os.makedirs(pasta_imagens, exist_ok=True)
    os.makedirs(pasta_pdfs, exist_ok=True)

    # ========== MENU LATERAL ==========
    menu = tk.Frame(main, bg="#4D908E", width=200)
    menu.pack(side="left", fill="y")

    tk.Label(
        menu,
        text="📚 GERENCIAR LIVROS",
        bg="#4D908E",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    def abrir_home():
        # limpa a janela atual e abre a home no mesmo root
        for widget in main.winfo_children():
            widget.destroy()
        home_page(main, usuario_email)

    def sair():
        main.destroy()

    botoes = [
        ("🏠 Ir para Home", abrir_home),
        ("🚪 Sair", sair)
    ]
    for texto, cmd in botoes:
        tk.Button(
            menu,
            text=texto,
            command=cmd,
            width=20,
            bg="#4D908E",
            fg="white",
            relief="flat",
            font=("Arial", 11),
            cursor="hand2"
        ).pack(pady=10)

    # ========== CONTEÚDO PRINCIPAL ==========
    conteudo = tk.Frame(main, bg="white")
    conteudo.pack(side="right", fill="both", expand=True)

    tk.Label(conteudo, text="Cadastro de Livros", bg="white", font=("Arial", 16, "bold")).pack(pady=10)

    form_frame = tk.Frame(conteudo, bg="white")
    form_frame.pack(pady=10)

    # ===== Campos =====
    tk.Label(form_frame, text="Título:", bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    titulo_entry = tk.Entry(form_frame, width=50)
    titulo_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Autor:", bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    autor_entry = tk.Entry(form_frame, width=50)
    autor_entry.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Disponível:", bg="white").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    disponivel_var = tk.StringVar(value="Sim")
    tk.OptionMenu(form_frame, disponivel_var, "Sim", "Não").grid(row=2, column=1, sticky="w", pady=5)

    # ===== Selecionar imagem =====
    imagem_caminho = tk.StringVar()

    def selecionar_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecionar Imagem da Capa",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")],
            initialdir=os.getcwd()
        )
        if caminho:
            imagem_caminho.set(caminho)
            try:
                img = Image.open(caminho).resize((80, 100))
                preview = ImageTk.PhotoImage(img)
                lbl_preview.config(image=preview)
                lbl_preview.image = preview
            except Exception:
                lbl_preview.config(image="")

    tk.Button(
        form_frame,
        text="📷 Selecionar Capa",
        command=selecionar_imagem,
        bg="#4D908E",
        fg="white"
    ).grid(row=3, column=0, pady=10)

    lbl_preview = tk.Label(form_frame, bg="white")
    lbl_preview.grid(row=3, column=1, pady=10)

    # ===== Selecionar PDF =====
    pdf_caminho = tk.StringVar()

    def selecionar_pdf():
        caminho = filedialog.askopenfilename(
            title="Selecionar PDF do Livro",
            filetypes=[("Arquivos PDF", "*.pdf")],
            initialdir=os.getcwd()
        )
        if caminho:
            pdf_caminho.set(caminho)
            lbl_pdf.config(text=f"📄 {os.path.basename(caminho)}")

    tk.Button(
        form_frame,
        text="📘 Anexar PDF",
        command=selecionar_pdf,
        bg="#4D908E",
        fg="white"
    ).grid(row=4, column=0, pady=5)

    lbl_pdf = tk.Label(form_frame, text="", bg="white", fg="gray", font=("Arial", 10, "italic"))
    lbl_pdf.grid(row=4, column=1, pady=5)

    # ===== Função salvar =====
    def salvar_livro():
        titulo = titulo_entry.get().strip()
        autor = autor_entry.get().strip()
        disponivel = disponivel_var.get()
        imagem = imagem_caminho.get()
        pdf = pdf_caminho.get()

        if not titulo or not autor:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return

        caminho_final_img = None
        if imagem:
            nome_img = os.path.basename(imagem)
            caminho_final_img = os.path.join(pasta_imagens, nome_img)
            try:
                shutil.copy(imagem, caminho_final_img)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao copiar imagem: {e}")
                return

        caminho_final_pdf = None
        if pdf:
            nome_pdf = os.path.basename(pdf)
            caminho_final_pdf = os.path.join(pasta_pdfs, nome_pdf)
            try:
                shutil.copy(pdf, caminho_final_pdf)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao copiar PDF: {e}")
                return

        inserir_livro(titulo, autor, disponivel, caminho_final_img, caminho_final_pdf)
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")
        atualizar_lista()

        # Limpar campos
        titulo_entry.delete(0, tk.END)
        autor_entry.delete(0, tk.END)
        disponivel_var.set("Sim")
        imagem_caminho.set("")
        pdf_caminho.set("")
        lbl_preview.config(image="")
        lbl_pdf.config(text="")

    tk.Button(
        form_frame,
        text="✅ Cadastrar Livro",
        command=salvar_livro,
        bg="#4D908E",
        fg="white",
        width=20
    ).grid(row=5, column=0, columnspan=2, pady=10)

    # ===== LISTA DE LIVROS =====
    tk.Label(conteudo, text="📚 Livros Cadastrados:", bg="white", font=("Arial", 13, "bold")).pack(pady=10)
    lista_frame = tk.Frame(conteudo, bg="white")
    lista_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(lista_frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="white")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ----- Helpers para editar -----
    def pegar_dados_livro(id_livro):
        """Retorna tupla do livro com id igual a id_livro ou None."""
        for l in listar_livros():
            if l[0] == id_livro:
                return l  # (id, titulo, autor, disponivel, imagem, pdf_path)
        return None

    def abrir_editar_dialog(id_livro):
        dados = pegar_dados_livro(id_livro)
        if not dados:
            messagebox.showerror("Erro", "Livro não encontrado.")
            return
        _, titulo_atual, autor_atual, disponivel_atual, imagem_atual, pdf_atual = dados

        dlg = tk.Toplevel(main)
        dlg.title(f"Editar - {titulo_atual}")
        dlg.geometry("480x380")
        dlg.transient(main)

        tk.Label(dlg, text="Título:").pack(anchor="w", padx=10, pady=(10, 0))
        ent_titulo = tk.Entry(dlg, width=60)
        ent_titulo.pack(padx=10, pady=5)
        ent_titulo.insert(0, titulo_atual)

        tk.Label(dlg, text="Autor:").pack(anchor="w", padx=10, pady=(10, 0))
        ent_autor = tk.Entry(dlg, width=60)
        ent_autor.pack(padx=10, pady=5)
        ent_autor.insert(0, autor_atual)

        tk.Label(dlg, text="Disponível:").pack(anchor="w", padx=10, pady=(10, 0))
        dispon_var = tk.StringVar(value=disponivel_atual)
        tk.OptionMenu(dlg, dispon_var, "Sim", "Não").pack(padx=10, pady=5, anchor="w")

        # trocar imagem/pdf
        new_img_path_var = tk.StringVar(value=imagem_atual or "")
        new_pdf_path_var = tk.StringVar(value=pdf_atual or "")

        def trocar_imagem():
            caminho = filedialog.askopenfilename(title="Selecionar nova capa", filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")])
            if caminho:
                new_img_path_var.set(caminho)
                tk.Label(dlg, text=f"Capa: {os.path.basename(caminho)}").pack()

        def trocar_pdf():
            caminho = filedialog.askopenfilename(title="Selecionar novo PDF", filetypes=[("PDF", "*.pdf")])
            if caminho:
                new_pdf_path_var.set(caminho)
                tk.Label(dlg, text=f"PDF: {os.path.basename(caminho)}").pack()

        tk.Button(dlg, text="📷 Trocar capa", command=trocar_imagem, bg="#4D908E", fg="white").pack(pady=6)
        tk.Button(dlg, text="📘 Trocar PDF", command=trocar_pdf, bg="#4D908E", fg="white").pack(pady=6)

        def salvar_edicao():
            novo_titulo = ent_titulo.get().strip()
            novo_autor = ent_autor.get().strip()
            novo_disp = dispon_var.get()
            img_src = new_img_path_var.get() or None
            pdf_src = new_pdf_path_var.get() or None

            # copiar arquivos para pastas da aplicação (se vieram de caminhos externos)
            caminho_final_img = imagem_atual
            caminho_final_pdf = pdf_atual

            if img_src and img_src != imagem_atual:
                nome_img = os.path.basename(img_src)
                caminho_final_img = os.path.join(pasta_imagens, nome_img)
                try:
                    shutil.copy(img_src, caminho_final_img)
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao copiar imagem: {e}")
                    return

            if pdf_src and pdf_src != pdf_atual:
                nome_pdf = os.path.basename(pdf_src)
                caminho_final_pdf = os.path.join(pasta_pdfs, nome_pdf)
                try:
                    shutil.copy(pdf_src, caminho_final_pdf)
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao copiar PDF: {e}")
                    return

            try:
                editar_livro(id_livro, novo_titulo, novo_autor, novo_disp, caminho_final_img, caminho_final_pdf)
                messagebox.showinfo("Sucesso", "Livro atualizado.")
                dlg.destroy()
                atualizar_lista()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao atualizar livro: {e}")

        tk.Button(dlg, text="💾 Salvar Alterações", bg="#4D908E", fg="white", command=salvar_edicao).pack(pady=12)

    # ----- atualizar lista -----
    def atualizar_lista():
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        livros = listar_livros()
        if not livros:
            tk.Label(scroll_frame, text="Nenhum livro cadastrado.", bg="white", fg="gray").pack(pady=20)
            return

        for id_livro, titulo, autor, disponivel, imagem, pdf_path in livros:
            card = tk.Frame(scroll_frame, bg="#eef5f5", relief="solid", bd=1)
            card.pack(fill="x", padx=10, pady=5)

            # Imagem de capa
            if imagem and os.path.exists(imagem):
                try:
                    img = Image.open(imagem).resize((60, 80))
                    capa = ImageTk.PhotoImage(img)
                except Exception:
                    capa = ImageTk.PhotoImage(Image.new("RGB", (60, 80), "#ccc"))
            else:
                capa = ImageTk.PhotoImage(Image.new("RGB", (60, 80), "#ccc"))

            lbl_capa = tk.Label(card, image=capa, bg="#eef5f5")
            lbl_capa.image = capa
            lbl_capa.pack(side="left", padx=10, pady=10)

            info = tk.Frame(card, bg="#eef5f5")
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=titulo, font=("Arial", 13, "bold"), bg="#eef5f5").pack(anchor="w")
            tk.Label(info, text=f"Autor: {autor}", bg="#eef5f5").pack(anchor="w")
            tk.Label(info, text=f"Disponível: {disponivel}", bg="#eef5f5").pack(anchor="w")

            # ===== BOTÃO "LER LIVRO" =====
            if pdf_path and os.path.exists(pdf_path):
                tk.Button(
                    info,
                    text="📖 Ler Livro",
                    bg="#4D908E",
                    fg="white",
                    cursor="hand2",
                    command=lambda id=id_livro, t=titulo: leitura_page(main, usuario_email, id, t)
                ).pack(anchor="w", pady=3)
            else:
                tk.Label(info, text="📄 PDF não disponível", bg="#eef5f5", fg="gray").pack(anchor="w")

            botoes_frame = tk.Frame(card, bg="#eef5f5")
            botoes_frame.pack(side="right", padx=10)
            tk.Button(
                botoes_frame,
                text="✏️ Editar",
                bg="#4D908E",
                fg="white",
                command=lambda id=id_livro: abrir_editar_dialog(id)
            ).pack(side="left", padx=5)
            tk.Button(
                botoes_frame,
                text="🗑️ Excluir",
                bg="#c84b4b",
                fg="white",
                command=lambda id=id_livro, t=titulo: confirmar_excluir(id, t)
            ).pack(side="left", padx=5)

    def confirmar_excluir(id_livro, titulo):
        if messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja excluir '{titulo}'?"):
            try:
                excluir_livro(id_livro)
                messagebox.showinfo("Removido", f"'{titulo}' excluído.")
                atualizar_lista()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir: {e}")

    atualizar_lista()

    if master is None:
        main.mainloop()
