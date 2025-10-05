import tkinter as tk
from tkinter import messagebox
from banco import verificar_login, conectar
import main
import cadastro

def abrir_cadastro():
    janela_login.destroy()
    cadastro.abrir_cadastro()

def login():
    email_valor = campo_email.get()
    senha_valor = campo_senha.get()
    manter_logado = var_manter_logado.get()

    if verificar_login(email_valor, senha_valor):
        msg = "Login bem-sucedido!"
        if manter_logado:
            msg += " (Manter logado)"
        messagebox.showinfo("Sucesso", msg)
        janela_login.destroy()
        main.abrir_interface()
    else:
        messagebox.showerror("Erro", "E-mail ou senha incorretos")

def abrir_login():
    global janela_login, campo_email, campo_senha, var_manter_logado

    conectar()

    janela_login = tk.Tk()
    janela_login.title("Login")
    janela_login.geometry("600x550")
    janela_login.configure(bg="#f4f4f4")

    tk.Label(janela_login, text="Login", font=("Arial", 38, "bold"), fg="#006666", bg="#f4f4f4").pack(pady=30)

    tk.Label(janela_login, text="Seu e-mail:", font=("Arial", 20), bg="#f4f4f4").pack()
    campo_email = tk.Entry(janela_login, font=("Arial", 20), width=30)
    campo_email.pack(pady=12)

    tk.Label(janela_login, text="Sua senha:", font=("Arial", 20), bg="#f4f4f4").pack()
    campo_senha = tk.Entry(janela_login, show="*", font=("Arial", 20), width=30)
    campo_senha.pack(pady=12)

    var_manter_logado = tk.BooleanVar()
    tk.Checkbutton(janela_login, text="Manter-me logado", variable=var_manter_logado, font=("Arial", 18), bg="#f4f4f4").pack(pady=12)

    tk.Button(janela_login, text="Logar", bg="#339999", fg="white", font=("Arial", 20, "bold"), width=20, height=2, command=login).pack(pady=25)

    tk.Label(janela_login, text="Ainda não tem conta?", font=("Arial", 18), bg="#f4f4f4").pack()
    tk.Button(janela_login, text="Cadastre-se", fg="blue", font=("Arial", 18, "bold"), bg="#e0e0e0", borderwidth=0, command=abrir_cadastro).pack()

    janela_login.mainloop()

if __name__ == "__main__":
    abrir_login()
