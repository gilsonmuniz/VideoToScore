import librosa
import librosa.display
import numpy as np

def detectar_notas(y, sr):
    # Detectar as frequências das notas (pode detectar múltiplas notas)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    notas_detectadas = []

    # Loop para cada quadro e detectar notas
    for t in range(magnitudes.shape[1]):
        # Pega as magnitudes das frequências para o quadro t
        pitch_values = pitches[:, t]
        magnitude_values = magnitudes[:, t]

        # Filtrar frequências significativas (com magnitude maior que um threshold)
        significant_pitches = pitch_values[magnitude_values > np.median(magnitude_values)]

        # Verifique as frequências detectadas
        print(f"Frame {t}: Frequências detectadas: {significant_pitches}")

        # Para cada pitch significativo, converter para nota
        for pitch in significant_pitches:
            if pitch > 0:
                nota = librosa.hz_to_note(pitch)
                notas_detectadas.append((nota, t))
    
    return notas_detectadas

def calcular_duracao(notas_detectadas):
    duracoes = []
    for i in range(len(notas_detectadas)):
        if i + 1 < len(notas_detectadas):
            # Se for a mesma nota e dentro de um pequeno intervalo de tempo, é a mesma nota
            if notas_detectadas[i][0] == notas_detectadas[i + 1][0]:
                duracoes.append((notas_detectadas[i + 1][1] - notas_detectadas[i][1]) / 50.0)  # A duração estimada em segundos
    return duracoes

music_name = input("Insira o nome da música: ")

# Carregar o áudio
y, sr = librosa.load("audios/{}.wav".format(music_name))

# Detectar as notas tocadas simultaneamente
notas_detectadas = detectar_notas(y, sr)

# Agrupar as notas simultâneas por tempo
notas_simultaneas = []
tempo_maximo = 20  # Tolerância de tempo para considerar as notas simultâneas

for t in range(0, len(notas_detectadas), tempo_maximo):
    notas_simultaneas.append(notas_detectadas[t:t + tempo_maximo])

# Abrir o arquivo para escrita
with open("texts/{}.txt".format(music_name), 'w') as file:
    # Escrever notas simultâneas e suas durações
    for notas in notas_simultaneas:
        notas_unicas = list(set([nota[0] for nota in notas]))
        duracoes = calcular_duracao(notas)

        # Escrever as notas e durações na mesma linha
        file.write("Notas: ")
        file.write(", ".join([f"Nota: {nota} | Duração: {duracao:.2f} s" for nota, duracao in zip(notas_unicas, duracoes)]))
        file.write("\n")
