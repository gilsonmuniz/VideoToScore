import xml.etree.ElementTree as ET

STANDARD_NOTES_VALUES = (
    1, # semifusa
    2, # fusa
    4, # semicolcheia
    8, # colcheia
    16, # semínima
    32, # mínima
    64 # semibreve
)

DIVISIONS = 1 # Base de divisão para a menor nota (semifusa = 1)

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

def get_base_and_dot(duration):
    return duration, duration not in STANDARD_NOTES_VALUES

def create_note_element(step, alter, octave, duration_value):
    base_value, dotted = get_base_and_dot(duration_value)

    note = ET.Element("note")
    pitch = ET.SubElement(note, "pitch")
    ET.SubElement(pitch, "step").text = step
    if alter != 0:
        ET.SubElement(pitch, "alter").text = str(alter)
    ET.SubElement(pitch, "octave").text = str(octave)

    ET.SubElement(note, "duration").text = str(duration_value)
    ET.SubElement(note, "type").text = note_type_from_duration(base_value)
    if dotted:
        ET.SubElement(note, "dot")
    return note

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
        return standard_types[duration]

def build_xml(music_dict):
    score = ET.Element('score-partwise', version='3.1')
    part_list = ET.SubElement(score, 'part-list')
    score_part = ET.SubElement(part_list, 'score-part', id='P1')
    ET.SubElement(score_part, 'part-name').text = 'Music'

    part = ET.SubElement(score, 'part', id='P1')

    # Unifica as notas por instante para ordenar
    all_notes = []
    for note_name, data in music_dict.items():
        for instant, duration in zip(data['instants'], data['durations']):
            all_notes.append((instant, duration, note_name))
    all_notes.sort()

    measure = None
    current_time = 0
    measure_number = 1
    measure_duration = 64 # 4/4, com semibreve como base (64 = semibreve)

    time_in_measure = 0

    for instant, duration, note_name in all_notes:
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

        step, alter, octave = parse_note_name(note_name)
        note_element = create_note_element(step, alter, octave, duration)
        measure.append(note_element)
        time_in_measure += duration

    tree = ET.ElementTree(score)
    tree.write('../xmls/output.xml', encoding='utf-8', xml_declaration=True)
