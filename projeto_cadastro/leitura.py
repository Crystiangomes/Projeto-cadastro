import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import webbrowser
from banco import obter_pdf_livro


def leitura_page(root, usuario_email, id_livro, titulo):
    """Tela de leitura de livros (abre PDF, salva progresso e permite voltar)"""

    # ======= LIMPAR A JANELA ATUAL =======
    for widget in root.winfo_children():
        widget.destroy()
    root.update_idletasks()

    root.title(f"Lendo: {titulo}")
    root.geometry("950x650")
    root.configure(bg="#F8F9FA")

    frame = tk.Frame(root, bg="#F8F9FA")
    frame.pack(fill="both", expand=True, padx=30, pady=20)

    tk.Label(frame, text=f"📖 {titulo}", font=("Arial", 22, "bold"), bg="#F8F9FA").pack(pady=15)

    # ======= OBTÉM O PDF DO BANCO =======
    pdf_path = obter_pdf_livro(id_livro)
    if pdf_path:
        pdf_path = os.path.abspath(pdf_path)
    if not pdf_path or not os.path.exists(pdf_path):
        tk.Label(frame, text="⚠️ O arquivo PDF deste livro não foi encontrado.", fg="red", bg="#F8F9FA").pack(pady=10)
        tk.Button(
            frame, text="⬅️ Voltar", bg="#B56576", fg="white",
            width=15, cursor="hand2", command=lambda: voltar_para_home(root, usuario_email)
        ).pack(pady=25)
        return

    # ======= ARQUIVO DE PROGRESSO =======
    progresso_path = f"progresso_{usuario_email.replace('@', '_').replace('.', '_')}.txt"

    def obter_pagina_salva():
        """Lê o progresso salvo do usuário para o livro atual"""
        if not os.path.exists(progresso_path):
            return None
        with open(progresso_path, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.startswith(f"{id_livro}|"):
                    partes = linha.strip().split("|")
                    if len(partes) > 2:
                        return partes[2]
        return None

    def salvar_pagina():
        """Salva a página atual digitada"""
        pagina = entrada_pagina.get().strip()
        if not pagina.isdigit():
            messagebox.showerror("Erro", "Digite um número de página válido.")
            return

        linhas = []
        if os.path.exists(progresso_path):
            with open(progresso_path, "r", encoding="utf-8") as f:
                linhas = f.readlines()

        with open(progresso_path, "w", encoding="utf-8") as f:
            atualizado = False
            for linha in linhas:
                if linha.startswith(f"{id_livro}|"):
                    f.write(f"{id_livro}|{titulo}|{pagina}\n")
                    atualizado = True
                else:
                    f.write(linha)
            if not atualizado:
                f.write(f"{id_livro}|{titulo}|{pagina}\n")

        messagebox.showinfo("Progresso Salvo", f"Página {pagina} marcada como última lida.")

    # ======= FUNÇÕES DE LEITURA E DOWNLOAD =======
    def ler_pdf():
        """Abre o PDF no leitor padrão do sistema"""
        try:
            webbrowser.open_new(pdf_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF:\n{e}")

    def baixar_pdf():
        """Permite salvar o PDF localmente"""
        destino = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")],
            initialfile=os.path.basename(pdf_path),
            title="Salvar livro"
        )
        if destino:
            try:
                shutil.copy(pdf_path, destino)
                messagebox.showinfo("Download concluído", f"O livro foi salvo em:\n{destino}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o PDF:\n{e}")

    # ======= BOTÕES DE AÇÃO =======
    botoes_frame = tk.Frame(frame, bg="#F8F9FA")
    botoes_frame.pack(pady=20)

    tk.Button(
        botoes_frame, text="📖 Ler Agora", bg="#4D908E", fg="white",
        width=15, cursor="hand2", command=ler_pdf
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        botoes_frame, text="⬇️ Baixar PDF", bg="#577590", fg="white",
        width=15, cursor="hand2", command=baixar_pdf
    ).grid(row=0, column=1, padx=10)

    # ======= MARCADOR DE PÁGINA =======
    marcador_frame = tk.Frame(frame, bg="#F8F9FA")
    marcador_frame.pack(pady=20)

    tk.Label(marcador_frame, text="📍 Página atual:", bg="#F8F9FA", font=("Arial", 12)).grid(row=0, column=0, padx=5)
    entrada_pagina = tk.Entry(marcador_frame, width=10)
    entrada_pagina.grid(row=0, column=1, padx=5)

    tk.Button(
        marcador_frame, text="💾 Salvar", bg="#4D908E", fg="white",
        command=salvar_pagina
    ).grid(row=0, column=2, padx=5)

    pagina_salva = obter_pagina_salva()
    if pagina_salva:
        tk.Label(
            frame, text=f"📘 Última página salva: {pagina_salva}",
            bg="#F8F9FA", fg="gray", font=("Arial", 11)
        ).pack(pady=10)

    # ======= BOTÃO VOLTAR =======
    tk.Button(
        frame, text="⬅️ Voltar", bg="#B56576", fg="white",
        width=15, cursor="hand2", command=lambda: voltar_para_home(root, usuario_email)
    ).pack(pady=25)


def voltar_para_home(root, usuario_email):
    """Retorna à tela principal sem duplicar widgets"""
    for widget in root.winfo_children():
        widget.destroy()
    root.update_idletasks()
    from home import home_page
    home_page(root, usuario_email)


# ======= TESTE DIRETO =======
if __name__ == "__main__":
    root = tk.Tk()
    leitura_page(root, "teste@exemplo.com", 1, "Livro Exemplo")
    root.mainloop()
