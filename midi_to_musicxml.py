from music21 import converter, midi

# Função para converter o arquivo MIDI em MusicXML
def midi_to_musicxml(midi_file, musicxml_file):
    # Carregar o arquivo MIDI usando music21
    midi_data = converter.parse(midi_file)

    # Converter para MusicXML e salvar
    midi_data.write('musicxml', fp=musicxml_file)

# Exemplo de uso
midi_file = 'midis/heart_and_soul_resampled.midi'  # Substitua com o nome correto do arquivo MIDI
musicxml_file = 'xmls/heart_and_soul_resampled.xml'  # Nome do arquivo de saída em MusicXML
midi_to_musicxml(midi_file, musicxml_file)
