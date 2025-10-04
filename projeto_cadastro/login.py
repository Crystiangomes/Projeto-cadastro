import tkinter as tk
from tkinter import messagebox
from banco import verificar_login, conectar
import cadastro_usuario
import main # executa o arquivo todo

# from cadastro_usuario import validar_cadastro


def janela_cadastro():
    """Abre a tela de cadastro de usuários."""
    # Fecha a tela de login atual (se estiver aberta)
    root.destroy()
    # cadastro_usuario.janela_cadastro.mainloop()  # chama a função da tela de cadastro

def login():
    """Verifica login e abre a tela principal."""
    email_valor = campo_email.get().strip()
    senha_valor = campo_senha.get().strip()
    manter_logado = var_manter_logado.get()

    if verificar_login(email_valor, senha_valor):
        msg = "Login bem-sucedido!"
        if manter_logado:
            msg += " (Manter logado)"
        messagebox.showinfo("Sucesso", msg)

        root.destroy()

        # Aqui você precisa ajustar para a função que realmente abre a tela principal
        # No seu main.py não existe abrir_main(), então usamos a janela principal diretamente
        #
        main.janela.deiconify()  # <- Certifique-se que 'janela' está criada no main.py
    else:
        messagebox.showerror("Erro", "E-mail ou senha incorretos")

def janela_login():
    """Cria a tela de login."""
    global root, campo_email, campo_senha, var_manter_logado

    conectar()  # garante que o banco existe

    root = tk.Tk()
    root.title("Login")
    root.geometry("600x550")
    root.configure(bg="#f4f4f4")

    tk.Label(root, text="Login", font=("Arial", 38, "bold"), fg="#006666", bg="#f4f4f4").pack(pady=30)

    tk.Label(root, text="Seu e-mail:", font=("Arial", 20), bg="#f4f4f4").pack()
    campo_email = tk.Entry(root, font=("Arial", 20), width=30)
    campo_email.pack(pady=12)

    tk.Label(root, text="Sua senha:", font=("Arial", 20), bg="#f4f4f4").pack()
    campo_senha = tk.Entry(root, show="*", font=("Arial", 20), width=30)
    campo_senha.pack(pady=12)

    var_manter_logado = tk.BooleanVar()
    tk.Checkbutton(root, text="Manter-me logado", variable=var_manter_logado,
                   font=("Arial", 18), bg="#f4f4f4").pack(pady=12)

    tk.Button(root, text="Logar", bg="#339999", fg="white",
              font=("Arial", 20, "bold"), width=20, height=2,
              command=login).pack(pady=25)

    tk.Label(root, text="Ainda não tem conta?", font=("Arial", 18), bg="#f4f4f4").pack()

    tk.Button(root, text="Cadastre-se", fg="blue", font=("Arial", 18, "bold"),
              bg="#e0e0e0", borderwidth=0, command=janela_cadastro).pack()

    root.mainloop()


janela_login()
