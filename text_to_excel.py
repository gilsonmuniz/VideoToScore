# -*- coding: utf-8 -*-

import pandas as pd
import re

# Ordenação das notas musicais
notas_ordenadas = [
    "{}{}".format(nota, oitava) for oitava in range(8)
    for nota in ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
]

music_name = input("Insira o nome da música: ")

# Lendo o arquivo de entrada
with open("texts/{}.txt".format(music_name), "r", encoding="utf-8") as file:
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
df.to_excel("excels/{}.xlsx".format(music_name), index=False)
