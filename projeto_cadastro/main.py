import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from banco import inserir, listar, excluir, editar, criar_tabela


id_editando = None
caminho_imagem = None

# ================= Funções =================

def listar_livros():
    lista.delete(0, tk.END)
    for livro in listar():
        lista.insert(tk.END, f"{livro[0]} | {livro[1]} | {livro[2]} | {livro[3]} | {livro[4]}")
    lista.selection_clear(0, tk.END)

def salvar():
    global caminho_imagem
    if titulo.get() and autor.get() and disponivel.get():
        inserir(titulo.get(), autor.get(), disponivel.get(), caminho_imagem)
        listar_livros()
        limpar()
        mostrar_status("✅ Livro salvo com sucesso!", "#28a745")
    else:
        mostrar_status("⚠️ Preencha todos os campos!", "#d9534f")

def excluir_livro():
    sel = lista.curselection()
    if sel:
        livro = lista.get(sel)
        id_livro = livro.split(" | ")[0]
        excluir(id_livro)
        listar_livros()
        limpar()
        mostrar_status("🗑️ Livro excluído com sucesso!", "#dc3545")
    else:
        mostrar_status("⚠️ Selecione um livro para excluir.", "#d9534f")

def editar_livro():
    sel = lista.curselection()
    if sel:
        livro = lista.get(sel).split(" | ")
        global id_editando, caminho_imagem
        id_editando = livro[0]
        titulo.set(livro[1])
        autor.set(livro[2])
        disponivel.set(livro[3])
        caminho_imagem = livro[4]
        mostrar_status(f"✏️ Editando livro ID: {id_editando}", "#007b7f")
    else:
        mostrar_status("⚠️ Selecione um livro para editar.", "#d9534f")

def salvar_edicao():
    global id_editando, caminho_imagem
    if titulo.get() and autor.get() and disponivel.get() and id_editando:
        editar(id_editando, titulo.get(), autor.get(), disponivel.get(), caminho_imagem)
        listar_livros()
        limpar()
        mostrar_status(f"✅ Edição salva para livro ID: {id_editando}", "#28a745")
        id_editando = None
    else:
        mostrar_status("⚠️ Complete os dados corretamente!", "#d9534f")

def limpar():
    global caminho_imagem
    titulo.set("")
    autor.set("")
    disponivel.set("")
    caminho_imagem = None
    lista.selection_clear(0, tk.END)
    label_status.configure(text="")

def mostrar_status(texto, cor):
    label_status.configure(text=texto, foreground=cor)

def escolher_imagem():
    global caminho_imagem
    caminho_imagem = filedialog.askopenfilename(
        title="Selecione a capa",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
    )
    if caminho_imagem:
        mostrar_status(f"📷 Capa selecionada: {caminho_imagem.split('/')[-1]}", "#007bff")

# ================= Tela Visão Geral =================
def abrir_visao_geral():
    janela.withdraw()
    vg = tk.Toplevel()
    vg.title("Visão Geral")
    vg.geometry("1000x700")
    vg.configure(bg="#f4f4f4")

    tk.Label(vg, text="📚 Livros Disponíveis", font=("Segoe UI", 18, "bold"), bg="#f4f4f4").pack(pady=15)

    frame_grid = tk.Frame(vg, bg="#f4f4f4")
    frame_grid.pack(fill="both", expand=True)

    livros = listar()
    colunas = 3
    row, col = 0, 0

    for livro in livros:
        card = tk.Frame(frame_grid, bg="white", width=250, height=280, highlightbackground="#aaa", highlightthickness=1)
        card.grid(row=row, column=col, padx=15, pady=15)

        # Capa
        if livro[4]:
            try:
                img = Image.open(livro[4])
                img = img.resize((120, 160))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(card, image=photo, bg="white")
                img_label.image = photo
                img_label.pack(pady=8)
            except:
                tk.Label(card, text="(sem capa)", bg="white").pack(pady=20)
        else:
            tk.Label(card, text="(sem capa)", bg="white").pack(pady=20)

        # Infos
        tk.Label(card, text=f"📖 {livro[1]}", bg="white", font=("Segoe UI", 12, "bold")).pack()
        tk.Label(card, text=f"✍️ {livro[2]}", bg="white", font=("Segoe UI", 11)).pack()
        tk.Label(card, text=f"Disponível: {livro[3]}", bg="white", font=("Segoe UI", 10)).pack()

        tk.Button(card, text="📦 Pegar emprestado", bg="#6e9ea0", fg="white",
          command=lambda l=livro: pegar_emprestado(l[0], l[1])).pack(pady=10)


        col += 1
        if col >= colunas:
            col = 0
            row += 1

    tk.Button(vg, text="← Voltar", command=lambda: (vg.destroy(), janela.deiconify()),
              bg="#6e9ea0", fg="white").pack(pady=20)

# ================= Janela Principal =================
janela = tk.Tk()
janela.title("Cadastro de Livros")
janela.geometry("1100x720")
janela.configure(bg="#f4f4f4")

# ---- Painel lateral
painel_lateral = tk.Frame(janela, bg="#6e9ea0", width=200)
painel_lateral.pack(side="left", fill="y")

logo_label = tk.Label(painel_lateral, text="\n📚\nBIBLIOTECA", bg="#6e9ea0", fg="white", font=("Segoe UI", 14, "bold"))
logo_label.pack(pady=20)

opcoes = [
    ("Visão Geral", "📊", abrir_visao_geral),
    ("Livros", "📚", None),
    ("Usuários", "👤", None),
    ("Empréstimos", "📦", None)
]
for texto, icone, comando in opcoes:
    btn = tk.Button(painel_lateral, text=f"{icone} {texto}", bg="#6e9ea0", fg="white",
             font=("Segoe UI", 11, "bold"), anchor="w", relief="flat", command=comando)
    btn.pack(fill="x", padx=20, pady=6)

# ---- Área principal
area_principal = tk.Frame(janela, bg="#f4f4f4")
area_principal.pack(side="left", fill="both", expand=True)

# ---- Card
card = tk.Frame(area_principal, bg="white", width=750, height=350, highlightbackground="#999", highlightthickness=1)
card.pack(pady=20)

tk.Label(card, text="Cadastro de Livros", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=15)

label_status = tk.Label(card, text="", font=("Segoe UI", 11, "italic"), bg="white")
label_status.pack(pady=5)

frame_inputs = tk.Frame(card, bg="white")
frame_inputs.pack(pady=5)

titulo = tk.StringVar()
autor = tk.StringVar()
disponivel = tk.StringVar()

def criar_input(label_texto, variavel):
    f = tk.Frame(frame_inputs, bg="white")
    f.pack(pady=5)
    tk.Label(f, text=label_texto, bg="white", width=18, anchor="e", font=("Segoe UI", 12)).pack(side="left")
    tk.Entry(f, textvariable=variavel, width=50, font=("Segoe UI", 12)).pack(side="left", padx=8)

criar_input("Título:", titulo)
criar_input("Autor:", autor)
criar_input("Disponível (Sim/Não):", disponivel)

btn_img = tk.Button(card, text="📷 Selecionar Capa", command=escolher_imagem, bg="#6e9ea0", fg="white")
btn_img.pack(pady=10)

frame_botoes = tk.Frame(card, bg="white")
frame_botoes.pack(pady=20)

def criar_botao(texto, comando):
    btn = tk.Button(frame_botoes, text=texto, command=comando, font=("Segoe UI", 11, "bold"), bg="#6e9ea0", fg="white",
                    activebackground="#4e7a7a", width=15)
    btn.pack(side="left", padx=10)

criar_botao("Salvar", salvar)
criar_botao("Editar", editar_livro)
criar_botao("Salvar Edição", salvar_edicao)
criar_botao("Excluir", excluir_livro)

def pegar_emprestado(livro_id, titulo_livro):
    messagebox.showinfo("Empréstimo Realizado", f"✅ Você pegou emprestado o livro:\n\n📖 {titulo_livro}")
    
    abrir_pagina_emprestimo(livro_id, titulo_livro)

def abrir_pagina_emprestimo(livro_id, titulo_livro):
    pg = tk.Toplevel()
    pg.title("Livro Emprestado")
    pg.geometry("500x300")
    pg.configure(bg="#f4f4f4")

    tk.Label(pg, text="📦 Empréstimo Confirmado", font=("Segoe UI", 18, "bold"), bg="#f4f4f4", fg="#28a745").pack(pady=20)
    tk.Label(pg, text=f"ID do Livro: {livro_id}", font=("Segoe UI", 13), bg="#f4f4f4").pack(pady=5)
    tk.Label(pg, text=f"Título: {titulo_livro}", font=("Segoe UI", 13), bg="#f4f4f4").pack(pady=5)

    tk.Button(pg, text="← Voltar", command=pg.destroy, bg="#6e9ea0", fg="white", font=("Segoe UI", 11, "bold")).pack(pady=30)


# ---- Lista
frame_lista = tk.Frame(area_principal, bg="#e1e1e1", width=800, height=250)
frame_lista.pack(pady=10)

tk.Label(frame_lista, text="📘 Livros Armazenados", font=("Segoe UI", 13, "bold"), bg="#e1e1e1").pack(pady=8)

lista = tk.Listbox(frame_lista, width=110, height=8, font=("Courier New", 11), bg="white",
                   selectbackground="#cfeef2", relief="flat")
lista.pack(pady=(0, 10))

# ---- Inicializar
criar_tabela()      # 🔥 Garante que a conexão e a tabela existam
listar_livros()
janela.mainloop()
