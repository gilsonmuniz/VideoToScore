import numpy as np
import aubio
import ffmpeg

# Nome do arquivo de áudio baixado
AUDIO_FILE = "audio.wav"

# Configuração do processamento
BUFFER_SIZE = 1024  # Tamanho do buffer do aubio
HOP_SIZE = BUFFER_SIZE  # Salto entre as janelas
RATE = 44100  # Taxa de amostragem

# Função para converter frequência em nota musical
def freq_to_note(freq):
    if freq > 0:
        note_number = 12 * np.log2(freq / 440.0) + 49
        note_number = round(note_number)
        notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        octave = (note_number // 12) - 1
        note = notes[note_number % 12]
        return f"{note}{octave}"
    return "Silêncio"

# Usa ffmpeg para converter áudio em fluxo de amostras
process = (
    ffmpeg.input(AUDIO_FILE)
    .output("pipe:", format="f32le", acodec="pcm_f32le", ac=1, ar=RATE)
    .run_async(pipe_stdout=True, pipe_stderr=True)
)

# Inicializa Aubio para detecção de pitch
pitch_o = aubio.pitch("default", BUFFER_SIZE, HOP_SIZE, RATE)
pitch_o.set_unit("Hz")
pitch_o.set_silence(-40)  # Define limite de silêncio

print("\nProcessando áudio...\n")

# Variáveis para calcular a duração da nota
current_note = None
start_time = 0
frame_count = 0

# Lê e processa o áudio
while True:
    raw_audio = process.stdout.read(HOP_SIZE * 4)  # 4 bytes por amostra (float32)
    if not raw_audio:
        break  # Fim do áudio

    samples = np.frombuffer(raw_audio, dtype=np.float32)

    # Garante que o tamanho da amostra seja 1024 antes de passar para o aubio
    if len(samples) < BUFFER_SIZE:
        samples = np.pad(samples, (0, BUFFER_SIZE - len(samples)))  # Preenche com zeros

    freq = pitch_o(samples)[0]

    # Filtro de ruído - Remove frequências irrelevantes
    if freq < 50 or freq > 4000:
        continue

    note = freq_to_note(freq)
    time_seconds = frame_count * (HOP_SIZE / RATE)

    # Se a nota mudou ou foi interrompida
    if note != current_note:
        if current_note is not None and current_note != "Silêncio":
            duration = time_seconds - start_time
            print(f"Nota: {current_note} | Duração: {duration:.2f} s")

        # Atualiza para a nova nota
        current_note = note
        start_time = time_seconds

    frame_count += 1

process.wait()
print("\nProcessamento concluído!")
