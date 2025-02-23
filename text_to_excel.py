# -*- coding: utf-8 -*-

import pandas as pd
import re

# Ordenação das notas musicais
notas_ordenadas = [
    "{}{}".format(nota, oitava) for oitava in range(8)
    for nota in ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
]

# Lendo o arquivo de entrada
with open("wicked_game.txt", "r", encoding="utf-8") as file:
    linhas = file.readlines()

# Processamento das notas
dados = []
padrao_nota = re.compile(r"Nota: (\D+\d)")

for linha in linhas:
    notas_encontradas = padrao_nota.findall(linha)
    linha_dados = {nota: 1 if nota in notas_encontradas else 0 for nota in notas_ordenadas}
    dados.append(linha_dados)

# Criando DataFrame e exportando para Excel
df = pd.DataFrame(dados, columns=notas_ordenadas)
df.to_excel("wicked_game.xlsx", index=False)
