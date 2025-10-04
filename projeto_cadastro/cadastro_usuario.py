# Importações necessárias
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import login


# Função de validação do cadastro
def validar_cadastro():
    """Função para validar os dados do cadastro"""
    # Coleta e limpeza dos dados digitados pelo usuário
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    senha = entry_senha.get()
    confirmar_senha = entry_confirmar_senha.get()

    # Valida se algum campo está vazio
    if not nome or not email or not senha or not confirmar_senha:
        messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios!")
        return
    
    # Validação básica de formato de e-mail
    if "@" not in email or "." not in email:
        messagebox.showerror("Erro de Cadastro", "Por favor, insira um e-mail válido!")
        return
    
    # Verifica se a senha tem o comprimento mínimo
    if len(senha) < 6:
        messagebox.showerror("Erro de Cadastro", "A senha deve ter pelo menos 6 caracteres!")
        return
    
    # Confirma se as senhas digitadas são iguais
    if senha != confirmar_senha:
        messagebox.showerror("Erro de Cadastro", "A senha e a confirmação de senha não coincidem!")
        return
    
    # Se tudo estiver correto, exibe mensagem de sucesso
    messagebox.showinfo("Cadastro Realizado", f"Usuário {nome} cadastrado com sucesso!")
    limpar_campos()

# Função que limpa os campos após cadastro
def limpar_campos():
    """Função para limpar todos os campos após cadastro bem-sucedido"""
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_confirmar_senha.delete(0, tk.END)
    entry_nome.focus()

# Função que permite submeter o formulário com a tecla Enter
def on_enter_key(event):
    """Função para permitir cadastro com Enter"""
    validar_cadastro()

# Criação da janela principal da aplicação
janela_cadastro = tk.Tk()
janela_cadastro.title("Cadastro de Usuário")
janela_cadastro.geometry("500x550")  # Aumentei um pouco o tamanho para melhor espaçamento
janela_cadastro.resizable(False, False)  # Janela não redimensionável para manter o layout
janela_cadastro.configure(bg="#f4f4f4")

# Configuração do estilo
style = ttk.Style()
style.theme_use('clam')

# Configurações de estilo personalizadas
style.configure('TFrame', background='#f4f4f4')
style.configure('TLabel', background='#f4f4f4', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
style.map('TButton', 
          background=[('active', '#3a5f5f'), ('!active', '#4e7a7a')],
          foreground=[('active', 'white'), ('!active', 'white')])

# Frame principal com sombra visual
main_frame = ttk.Frame(janela_cadastro, padding=(30, 20), style='TFrame')
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Cabeçalho do formulário
header_frame = ttk.Frame(main_frame, style='TFrame')
header_frame.pack(fill='x', pady=(0, 20))

# Ícone/Logo (simulado com um Label)
logo = tk.Label(header_frame, text="👤", font=('Arial', 24), bg='#f4f4f4')
logo.pack(side=tk.LEFT, padx=(0, 10))

# Título do formulário
titulo = tk.Label(header_frame, text="Crie sua conta", 
                 font=('Arial', 18, 'bold'), 
                 bg="#f4f4f4", fg='#2c3e3e')
titulo.pack(side=tk.LEFT)

# Frame dos campos de entrada com borda sutil
form_frame = ttk.Frame(main_frame, style='TFrame')
form_frame.pack(fill='x')

# ---------- Campo: Nome Completo ----------
label_nome = ttk.Label(form_frame, text="Nome Completo:", style='TLabel')
label_nome.grid(row=0, column=0, sticky="w", pady=(5, 2), padx=(0, 10))

entry_nome = ttk.Entry(form_frame, font=('Arial', 10), width=30)
entry_nome.grid(row=0, column=1, sticky="ew", pady=(5, 10), ipady=5)

# ---------- Campo: E-mail ----------
label_email = ttk.Label(form_frame, text="E-mail:", style='TLabel')
label_email.grid(row=1, column=0, sticky="w", pady=(5, 2), padx=(0, 10))

entry_email = ttk.Entry(form_frame, font=('Arial', 10), width=30)
entry_email.grid(row=1, column=1, sticky="ew", pady=(5, 10), ipady=5)

# ---------- Campo: Senha ----------
label_senha = ttk.Label(form_frame, text="Senha:", style='TLabel')
label_senha.grid(row=2, column=0, sticky="w", pady=(5, 2), padx=(0, 10))

entry_senha = ttk.Entry(form_frame, show="*", font=('Arial', 10), width=30)
entry_senha.grid(row=2, column=1, sticky="ew", pady=(5, 10), ipady=5)

# Dica de senha
senha_dica = ttk.Label(form_frame, text="Mínimo de 6 caracteres", 
                      style='TLabel', font=('Arial', 8))
senha_dica.grid(row=3, column=1, sticky="w", pady=(0, 10))

# ---------- Campo: Confirmar Senha ----------
label_confirmar_senha = ttk.Label(form_frame, text="Confirmar Senha:", style='TLabel')
label_confirmar_senha.grid(row=4, column=0, sticky="w", pady=(5, 2), padx=(0, 10))

entry_confirmar_senha = ttk.Entry(form_frame, show="*", font=('Arial', 10), width=30)
entry_confirmar_senha.grid(row=4, column=1, sticky="ew", pady=(5, 20), ipady=5)

 #Frame dos botões
botoes_frame = ttk.Frame(main_frame, style='TFrame')
botoes_frame.pack(fill='x', pady=(10, 0))

# Frame interno para centralizar os botões
botoes_inner_frame = ttk.Frame(botoes_frame, style='TFrame')
botoes_inner_frame.pack(expand=True)

# Botão de Limpar
btn_limpar = ttk.Button(botoes_inner_frame, text="LIMPAR", 
                      command=limpar_campos,
                      style='TButton')
btn_limpar.pack(side=tk.LEFT, ipadx=20, ipady=6, padx=(0, 10))

# Botão de Cadastrar
btn_cadastrar = ttk.Button(botoes_inner_frame, text="CADASTRAR", 
                         command=validar_cadastro,
                         style='TButton')
btn_cadastrar.pack(side=tk.LEFT, ipadx=20, ipady=6)

# Texto de rodapé (mantido igual)
footer = ttk.Label(main_frame, 
                  text="© 2025 Sistema de Cadastro. Todos os direitos reservados.",
                  style='TLabel', font=('Arial', 8))
footer.pack(side=tk.BOTTOM, pady=(20, 0))

# Permitir que Enter submeta o formulário
entry_nome.bind('<Return>', on_enter_key)
entry_email.bind('<Return>', on_enter_key)
entry_senha.bind('<Return>', on_enter_key)
entry_confirmar_senha.bind('<Return>', on_enter_key)

# Coloca o foco inicial no campo de nome
entry_nome.focus()

# Centraliza a janela na tela do usuário
janela_cadastro.update_idletasks()
width = janela_cadastro.winfo_width()
height = janela_cadastro.winfo_height()
x = (janela_cadastro.winfo_screenwidth() // 2) - (width // 2)
y = (janela_cadastro.winfo_screenheight() // 2) - (height // 2)
janela_cadastro.geometry(f'{width}x{height}+{x}+{y}')

# Inicia o loop principal da interface

