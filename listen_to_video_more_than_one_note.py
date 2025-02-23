import aubio
import numpy as np
from midiutil import MIDIFile

# Função para converter áudio para notas
def audio_to_midi(audio_file, output_file):
    # Configuração
    samplerate = 44100
    win_s = 1024
    hop_s = win_s // 2

    # Criação de objetos
    source = aubio.source(audio_file, samplerate, hop_s)
    pitch_detector = aubio.pitch("yin", win_s)
    pitch_detector.set_unit("Hz")
    pitch_detector.set_tolerance(0.8)

    # Inicialização do arquivo MIDI
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)  # Canal 0, tempo 120 BPM
    track = 0
    channel = 0
    time = 0  # tempo inicial no arquivo MIDI
    midi.addTrackName(track, time, "Track 1")

    # Processar o áudio para detecção de notas
    while True:
        samples, read = source()
        pitch = pitch_detector(samples)[0]

        if pitch != 0:  # Se uma nota for detectada
            # Convertendo o valor de pitch para um valor de nota MIDI inteiro
            pitch_int = int(round(pitch))  # Arredonda para o inteiro mais próximo
            if 0 <= pitch_int < 128:  # Verifica se a nota está no intervalo MIDI
                midi.addNote(track, channel, pitch_int, time, 1, 100)  # Nota: pitch, tempo, duração, volume

        time += 1
        if read < hop_s:
            break

    # Salvar o arquivo MIDI
    with open(output_file, "wb") as f:
        midi.writeFile(f)

# Exemplo de uso
music_name = input("Insira o nome da música: ")
audio_file = "audios/{}.wav".format(music_name)  # Substitua com o seu arquivo de áudio
output_file = "midis/{}.mid".format(music_name)  # Nome do arquivo MIDI de saída
audio_to_midi(audio_file, output_file)
