from music21 import converter

# Função para converter o arquivo MIDI para MusicXML
def midi_to_musicxml(midi_file, musicxml_file):
    # Carrega o arquivo MIDI
    midi_stream = converter.parse(midi_file)

    # Converte para MusicXML e salva
    midi_stream.write('musicxml', fp=musicxml_file)

# Exemplo de uso
music_name = input('Insira o nome da música: ')
midi_file = 'midis/{}.midi'.format(music_name)  # Arquivo MIDI de entrada
musicxml_file = 'xmls/{}.musicxml'.format(music_name)  # Arquivo MusicXML de saída
midi_to_musicxml(midi_file, musicxml_file)
