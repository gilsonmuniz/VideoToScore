import xml.etree.ElementTree as ET
from itertools import groupby

STANDARD_NOTES_VALUES = (
    1,  # semifusa
    2,  # fusa
    4,  # semicolcheia
    8,  # colcheia
    16, # semínima
    32, # mínima
    64  # semibreve
)

DIVISIONS = 1  # Base de divisão para a menor nota (semifusa = 1)

def parse_note_name(name):
    if len(name) == 2:
        step = name[0]
        alter = 0
        octave = int(name[1])
    else:
        step = name[0]
        alter = 1 if '#' in name else -1
        octave = int(name[-1])
    return step, alter, octave

def note_type_from_duration(duration):
    standard_types = {
        1: '64th',
        2: '32nd',
        4: '16th',
        8: 'eighth',
        16: 'quarter',
        32: 'half',
        64: 'whole'
    }

    if duration in STANDARD_NOTES_VALUES:
        return standard_types[duration], False
    closest_duration = max(k for k in standard_types if k <= duration)
    note_type = standard_types[closest_duration]
    return note_type, True

def create_note_element(step, alter, octave, duration_value):
    note_type, dotted = note_type_from_duration(duration_value)

    note = ET.Element('note')
    pitch = ET.SubElement(note, 'pitch')
    ET.SubElement(pitch, 'step').text = step
    if alter != 0:
        ET.SubElement(pitch, 'alter').text = str(alter)
    ET.SubElement(pitch, 'octave').text = str(octave)

    ET.SubElement(note, 'duration').text = str(duration_value)
    ET.SubElement(note, 'type').text = note_type
    if dotted:
        ET.SubElement(note, 'dot')
    return note

def build_xml(music_dict, xml_path):
    score = ET.Element('score-partwise', version='3.1')
    part_list = ET.SubElement(score, 'part-list')
    score_part = ET.SubElement(part_list, 'score-part', id='P1')
    ET.SubElement(score_part, 'part-name').text = 'Music'

    part = ET.SubElement(score, 'part', id='P1')

    # Agrupa todas as notas por instante
    all_notes = []
    for note_name, data in music_dict.items():
        for instant, duration in zip(data['instants'], data['durations']):
            all_notes.append((instant, duration, note_name))
    all_notes.sort()

    measure = None
    measure_number = 1
    measure_duration = 64  # 4/4, semibreve como unidade base
    time_in_measure = 0
    last_instant = 0  # Marca o tempo da última nota ou pausa adicionada

    for instant, group in groupby(all_notes, key=lambda x: x[0]):
        group = list(group)

        # Verifica se houve espaço vazio desde o último instante
        if instant > last_instant:
            silence_duration = instant - last_instant

            # Cria nova medida se necessário
            if measure is None or time_in_measure + silence_duration > measure_duration:
                measure = ET.SubElement(part, 'measure', number=str(measure_number))
                measure_number += 1
                attributes = ET.SubElement(measure, 'attributes')
                ET.SubElement(attributes, 'divisions').text = str(DIVISIONS)
                time = ET.SubElement(attributes, 'time')
                ET.SubElement(time, 'beats').text = '4'
                ET.SubElement(time, 'beat-type').text = '4'
                key = ET.SubElement(attributes, 'key')
                ET.SubElement(key, 'fifths').text = '0'
                clef = ET.SubElement(attributes, 'clef')
                ET.SubElement(clef, 'sign').text = 'G'
                ET.SubElement(clef, 'line').text = '2'
                time_in_measure = 0

            # Adiciona a pausa
            rest_note = ET.Element('note')
            ET.SubElement(rest_note, 'rest')
            ET.SubElement(rest_note, 'duration').text = str(silence_duration)
            note_type, dotted = note_type_from_duration(silence_duration)
            ET.SubElement(rest_note, 'type').text = note_type
            if dotted:
                ET.SubElement(rest_note, 'dot')
            measure.append(rest_note)
            time_in_measure += silence_duration

        # Cria nova medida se necessário antes de adicionar notas
        if measure is None or time_in_measure >= measure_duration:
            measure = ET.SubElement(part, 'measure', number=str(measure_number))
            measure_number += 1
            attributes = ET.SubElement(measure, 'attributes')
            ET.SubElement(attributes, 'divisions').text = str(DIVISIONS)
            time = ET.SubElement(attributes, 'time')
            ET.SubElement(time, 'beats').text = '4'
            ET.SubElement(time, 'beat-type').text = '4'
            key = ET.SubElement(attributes, 'key')
            ET.SubElement(key, 'fifths').text = '0'
            clef = ET.SubElement(attributes, 'clef')
            ET.SubElement(clef, 'sign').text = 'G'
            ET.SubElement(clef, 'line').text = '2'
            time_in_measure = 0

        # Adiciona as notas simultâneas (acordes)
        for i, (_, duration, note_name) in enumerate(group):
            step, alter, octave = parse_note_name(note_name)
            note_element = create_note_element(step, alter, octave, duration)
            if i > 0:
                ET.SubElement(note_element, 'chord')
            measure.append(note_element)

        time_in_measure += group[0][1]
        last_instant = instant + group[0][1]

    tree = ET.ElementTree(score)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
