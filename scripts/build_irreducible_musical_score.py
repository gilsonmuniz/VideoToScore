import xml.etree.ElementTree as ET
from itertools import groupby

DIVISIONS = 1  # 1 semifusa = 1 divisão

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

def create_note_element(step, alter, octave, tie_start=False, tie_stop=False):
    note = ET.Element('note')
    pitch = ET.SubElement(note, 'pitch')
    ET.SubElement(pitch, 'step').text = step
    if alter != 0:
        ET.SubElement(pitch, 'alter').text = str(alter)
    ET.SubElement(pitch, 'octave').text = str(octave)

    ET.SubElement(note, 'duration').text = '1'
    ET.SubElement(note, 'type').text = '64th'

    if tie_start:
        tie = ET.SubElement(note, 'tie', type="start")
    if tie_stop:
        tie = ET.SubElement(note, 'tie', type="stop")
    
    notations = None
    if tie_start or tie_stop:
        notations = ET.SubElement(note, 'notations')
    if tie_start:
        ET.SubElement(notations, 'tied', type="start")
    if tie_stop:
        ET.SubElement(notations, 'tied', type="stop")

    return note

def create_rest_element():
    rest_note = ET.Element('note')
    ET.SubElement(rest_note, 'rest')
    ET.SubElement(rest_note, 'duration').text = '1'
    ET.SubElement(rest_note, 'type').text = '64th'
    return rest_note

def build_irreducible_xml(music_dict, xml_path):
    score = ET.Element('score-partwise', version='3.1')
    part_list = ET.SubElement(score, 'part-list')
    score_part = ET.SubElement(part_list, 'score-part', id='P1')
    ET.SubElement(score_part, 'part-name').text = 'Music'

    part = ET.SubElement(score, 'part', id='P1')

    all_notes = []
    for note_name, data in music_dict.items():
        for instant, duration in zip(data['instants'], data['durations']):
            all_notes.append((instant, duration, note_name))
    all_notes.sort()

    measure = None
    measure_number = 1
    measure_duration = 64  # 4/4, 64 semifusas
    time_in_measure = 0
    last_instant = 0

    for instant, group in groupby(all_notes, key=lambda x: x[0]):
        group = list(group)

        if instant > last_instant:
            silence_duration = instant - last_instant
            for _ in range(silence_duration):
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
                measure.append(create_rest_element())
                time_in_measure += 1
            last_instant = instant

        max_duration = max(duration for _, duration, _ in group)

        for i in range(max_duration):
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

            for j, (_, duration, note_name) in enumerate(group):
                if i < duration:
                    step, alter, octave = parse_note_name(note_name)
                    tie_start = (i == 0 and duration > 1)
                    tie_stop = (i == duration - 1 and duration > 1)
                    note_element = create_note_element(step, alter, octave, tie_start=tie_start, tie_stop=tie_stop)
                    if j > 0:
                        ET.SubElement(note_element, 'chord')
                    measure.append(note_element)

            time_in_measure += 1
            last_instant += 1

    tree = ET.ElementTree(score)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
