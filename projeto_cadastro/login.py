import tkinter as tk
from tkinter import messagebox
from banco import verificar_login, conectar
import main
import cadastro

def abrir_cadastro():
    """Fecha a tela de login e abre a tela de cadastro."""
    janela_login.destroy()
    cadastro.abrir_cadastro()

def login():
    """Realiza a verificação de login e redireciona para o menu principal."""
    email_valor = campo_email.get().strip()
    senha_valor = campo_senha.get().strip()
    manter_logado = var_manter_logado.get()

    if not email_valor or not senha_valor:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    usuario = verificar_login(email_valor, senha_valor)

    if usuario:
        msg = "Login bem-sucedido!"
        if manter_logado:
            msg += " (Manter logado ativado)"
        messagebox.showinfo("Sucesso", msg)

        janela_login.destroy()

        # Abre a tela principal passando o e-mail do usuário logado
        main.main_page(email_valor)

    else:
        messagebox.showerror("Erro", "E-mail ou senha incorretos")

def abrir_login():
    """Cria a janela de login."""
    global janela_login, campo_email, campo_senha, var_manter_logado

    conectar()  # garante que o banco está disponível

    janela_login = tk.Tk()
    janela_login.title("Login - Biblioteca")
    janela_login.geometry("700x700")
    janela_login.configure(bg="#f4f4f4")
    janela_login.resizable(False, False)

    # Título
    tk.Label(janela_login, text="Login", font=("Arial", 38, "bold"), fg="#006666", bg="#f4f4f4").pack(pady=30)

    # Campo de e-mail
    tk.Label(janela_login, text="Seu e-mail:", font=("Arial", 20), bg="#f4f4f4").pack()
    campo_email = tk.Entry(janela_login, font=("Arial", 20), width=30)
    campo_email.pack(pady=12)

    # Campo de senha
    tk.Label(janela_login, text="Sua senha:", font=("Arial", 20), bg="#f4f4f4").pack()
    campo_senha = tk.Entry(janela_login, show="*", font=("Arial", 20), width=30)
    campo_senha.pack(pady=12)

    # Checkbox manter logado
    var_manter_logado = tk.BooleanVar()
    tk.Checkbutton(
        janela_login,
        text="Manter-me logado",
        variable=var_manter_logado,
        font=("Arial", 18),
        bg="#f4f4f4"
    ).pack(pady=12)

    # Botão de login
    tk.Button(
        janela_login,
        text="Entrar",
        bg="#339999",
        fg="white",
        font=("Arial", 20, "bold"),
        width=20,
        height=2,
        command=login
    ).pack(pady=25)

    # Link para cadastro
    tk.Label(janela_login, text="Ainda não tem conta?", font=("Arial", 18), bg="#f4f4f4").pack()
    tk.Button(
        janela_login,
        text="Cadastre-se",
        fg="blue",
        font=("Arial", 18, "bold"),
        bg="#e0e0e0",
        borderwidth=0,
        command=abrir_cadastro
    ).pack()

    janela_login.mainloop()

if __name__ == "__main__":
    abrir_login()
