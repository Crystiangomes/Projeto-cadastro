import tkinter as tk
from tkinter import messagebox
from banco import inserir_usuario
import login

def voltar():
    janela_cadastro.destroy()
    login.abrir_login()

def cadastrar():
    if not all([nome.get(), idade.get(), curso.get(), cep.get(), email.get(), senha.get()]):
        messagebox.showwarning("Campos vazios", "Preencha todos os campos!")
        return

    sucesso = inserir_usuario(nome.get(), idade.get(), curso.get(), cep.get(), email.get(), senha.get())

    if sucesso:
        for widget in janela_cadastro.winfo_children():
            widget.destroy()

        tk.Label(janela_cadastro, text="Cadastro realizado com sucesso!", font=("Arial", 16), bg="#f4f4f4", fg="green").pack(pady=30)
        tk.Button(janela_cadastro, text="Ir para Login", font=("Arial", 14), bg="#339999", fg="white", command=voltar).pack(pady=10)
    else:
        messagebox.showerror("Erro", "E-mail já cadastrado!")

def abrir_cadastro():
    global janela_cadastro, nome, idade, curso, cep, email, senha

    janela_cadastro = tk.Tk()
    janela_cadastro.title("Cadastro de Usuário")
    janela_cadastro.geometry("700x700")
    janela_cadastro.configure(bg="#f4f4f4")

    campos = [("Nome", "nome"), ("Idade", "idade"), ("Curso", "curso"), ("CEP", "cep"), ("Email", "email"), ("Senha", "senha")]

    entradas = {}
    for label, var in campos:
        tk.Label(janela_cadastro, text=label + ":", bg="#f4f4f4", font=("Arial", 14)).pack()
        entradas[var] = tk.Entry(janela_cadastro, width=30, font=("Arial", 14), show="*" if var == "senha" else "")
        entradas[var].pack(pady=5)

    nome, idade, curso, cep, email, senha = [entradas[k] for k in ["nome", "idade", "curso", "cep", "email", "senha"]]

    tk.Button(janela_cadastro, text="Cadastrar", bg="#339999", fg="white", font=("Arial", 14), command=cadastrar).pack(pady=20)
    tk.Button(janela_cadastro, text="Voltar", font=("Arial", 12), command=voltar).pack()

    janela_cadastro.mainloop()
