import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# --- "Banco de dados" fictício ---
usuarios = {
    "1": "João",
    "2": "Maria",
    "3": "Carlos"
}



livros = {
    "01": {"titulo": "Dom Casmurro", "disponivel": True},
    "02": {"titulo": "1984", "disponivel": True},
    "03": {"titulo": "O Senhor dos Anéis", "disponivel": True},
}

emprestimos = []  # lista que guardará os empréstimos

emprestimos.append

# --- Funções ---
def registrar_emprestimo():
    usuario_id = entry_usuario.get().strip()
    livro_id = entry_livro.get().strip()
    data_dev = entry_data.get().strip()

    if usuario_id not in usuarios:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return

    if livro_id not in livros:
        messagebox.showerror("Erro", "Livro não encontrado!")
        return

    if not livros[livro_id]["disponivel"]:
        messagebox.showerror("Erro", "Livro já emprestado!")
        return

    try:
        datetime.strptime(data_dev, "%d/%m/%Y")  # valida a data
    except ValueError:
        messagebox.showerror("Erro", "Data inválida! Use formato dd/mm/aaaa.")
        return

    # Registrar empréstimo
    emprestimos.append({
        "usuario": usuario_id,
        "livro": livro_id,
        "data_dev": data_dev
    })
    livros[livro_id]["disponivel"] = False

    atualizar_tabela()
    messagebox.showinfo("Sucesso", f"Empréstimo registrado para {usuarios[usuario_id]}.")


def atualizar_tabela():
    for item in tree.get_children():
        tree.delete(item)

    for emp in emprestimos:
        usuario = usuarios[emp["usuario"]]
        livro = livros[emp["livro"]]["titulo"]
        tree.insert("", "end", values=(emp["usuario"], usuario, emp["livro"], livro, emp["data_dev"]))


def limpar_campos():
    entry_usuario.delete(0, tk.END)
    entry_livro.delete(0, tk.END)
    entry_data.delete(0, tk.END)


# --- Interface Tkinter ---
root = tk.Tk()
root.title("Sistema de Biblioteca - Empréstimo")
root.geometry("800x500")

frame_form = tk.LabelFrame(root, text="Registrar Empréstimo", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=10)

tk.Label(frame_form, text="ID Usuário:").grid(row=0, column=0, sticky="w")
entry_usuario = tk.Entry(frame_form)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="ID Livro:").grid(row=1, column=0, sticky="w")
entry_livro = tk.Entry(frame_form)
entry_livro.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Data Devolução (dd/mm/aaaa):").grid(row=2, column=0, sticky="w")
entry_data = tk.Entry(frame_form)
entry_data.grid(row=2, column=1, padx=5, pady=5)

btn_registrar = tk.Button(frame_form, text="Registrar Empréstimo", bg="#2563eb", fg="white", command=registrar_emprestimo)
btn_registrar.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

btn_limpar = tk.Button(frame_form, text="Limpar", command=limpar_campos)
btn_limpar.grid(row=3, column=2, padx=5)

# --- Tabela de Empréstimos ---
frame_tab = tk.LabelFrame(root, text="Empréstimos Ativos", padx=10, pady=10)
frame_tab.pack(fill="both", expand=True, padx=10, pady=10)

cols = ("ID Usuário", "Nome", "ID Livro", "Título", "Data Devolução")
tree = ttk.Treeview(frame_tab, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)

root.mainloop()