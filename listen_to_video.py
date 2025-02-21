import numpy as np
import aubio
import pyaudio
import time

# Configuracao do audio
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100  # Taxa de amostragem
BUFFER_SIZE = 1024  # Tamanho do buffer

# Inicializa PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=BUFFER_SIZE)

# Inicializa Aubio para deteccao de pitch
pitch_o = aubio.pitch("default", BUFFER_SIZE, BUFFER_SIZE // 2, RATE)
pitch_o.set_unit("Hz")
pitch_o.set_silence(-40)  # Define o limite de silencio

# Funcao para converter frequencia em nota musical
def freq_to_note(freq):
    if freq > 0:
        note_number = 12 * np.log2(freq / 440.0) + 49
        note_number = round(note_number)
        notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        octave = (note_number // 12) - 1
        note = notes[note_number % 12]
        return f"{note}{octave}"
    return "Silencio"

print("Capturando audio...")

# Variaveis para calcular a duracao da nota
current_note = None
start_time = None

# Loop de deteccao em tempo real
while True:
    audio_data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
    samples = np.frombuffer(audio_data, dtype=np.float32)
    freq = pitch_o(samples)[0]
    
    note = freq_to_note(freq)

    # Se a nota mudou ou foi interrompida
    if note != current_note:
        if current_note is not None and current_note != "Silencio":
            duration = time.time() - start_time
            print(f"Nota: {current_note} | Duracao: {duration:.2f} s")
        
        # Atualiza para a nova nota
        current_note = note
        start_time = time.time()

    time.sleep(0.05)  # Pequeno delay para nao sobrecarregar o processamento
