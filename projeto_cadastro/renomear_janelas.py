import os
import re

# Usa a pasta onde o script está
pasta = os.path.dirname(os.path.abspath(__file__))

for arquivo in os.listdir(pasta):
    if arquivo.endswith(".py") and arquivo != os.path.basename(__file__):
        caminho_arquivo = os.path.join(pasta, arquivo)
        nome_base = os.path.splitext(arquivo)[0]
        novo_nome = f"janela_{nome_base}"

        backup_path = caminho_arquivo + ".bak"
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(conteudo)

        novo_conteudo = re.sub(r'\bjanela\b', novo_nome, conteudo)

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(novo_conteudo)

        print(f"✅ {arquivo}: 'janela' → '{novo_nome}'")

print("\n✨ Tudo pronto! Backups (.bak) criados na mesma pasta.")
