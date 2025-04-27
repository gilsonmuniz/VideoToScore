import xml.etree.ElementTree as ET
from itertools import groupby

DIVISIONS = 16  # Agora base é 16 para que a semifusa tenha duration=1

STANDARD_NOTES_VALUES = (1, 2, 4, 8, 16, 32, 64)


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


def create_single_note(step, alter, octave, voice, is_chord=False, tie_start=False, tie_stop=False, beam_type=None):
    note = ET.Element('note')

    if is_chord:
        ET.SubElement(note, 'chord')

    pitch = ET.SubElement(note, 'pitch')
    ET.SubElement(pitch, 'step').text = step
    if alter != 0:
        ET.SubElement(pitch, 'alter').text = str(alter)
    ET.SubElement(pitch, 'octave').text = str(octave)

    ET.SubElement(note, 'duration').text = '1'
    ET.SubElement(note, 'voice').text = str(voice)
    ET.SubElement(note, 'type').text = '64th'
    ET.SubElement(note, 'stem').text = 'up'

    if beam_type:
        ET.SubElement(note, 'beam', number='1').text = beam_type
        for i in range(2, 5):
            ET.SubElement(note, 'beam', number=str(i)).text = beam_type

    if tie_start or tie_stop:
        tie = ET.SubElement(note, 'tie', type='start' if tie_start else 'stop')
        notations = ET.SubElement(note, 'notations')
        ET.SubElement(notations, 'tied', type='start' if tie_start else 'stop')
        if tie_start and tie_stop:
            # Quando a nota ao mesmo tempo fecha um tie e abre outro
            notations.append(ET.Element('tied', {'type': 'stop'}))
            notations.append(ET.Element('tied', {'type': 'start'}))

    return note


def create_rest(voice, beam_type=None):
    rest = ET.Element('note')
    ET.SubElement(rest, 'rest')
    ET.SubElement(rest, 'duration').text = '1'
    ET.SubElement(rest, 'voice').text = str(voice)
    ET.SubElement(rest, 'type').text = '64th'
    if beam_type:
        ET.SubElement(rest, 'beam', number='1').text = beam_type
        for i in range(2, 5):
            ET.SubElement(rest, 'beam', number=str(i)).text = beam_type
    return rest


def build_irreducible_xml(music_dict, xml_path):
    score = ET.Element('score-partwise', version='3.1')
    part_list = ET.SubElement(score, 'part-list')
    score_part = ET.SubElement(part_list, 'score-part', id='P1')
    ET.SubElement(score_part, 'part-name').text = 'Music'

    part = ET.SubElement(score, 'part', id='P1')

    # Organiza todas as notas e pausas
    all_notes = []
    for note_name, data in music_dict.items():
        for instant, duration in zip(data['instants'], data['durations']):
            all_notes.append((instant, duration, note_name))
    all_notes.sort()

    measure = None
    measure_number = 1
    measure_duration = DIVISIONS * 4  # 4/4
    time_in_measure = 0
    last_instant = 0
    voice_counter = 1

    events = []

    # Primeiro gera todos os eventos de semifusas (inclusive pausas)
    for instant, group in groupby(all_notes, key=lambda x: x[0]):
        group = list(group)

        # Verifica espaço vazio -> pausa
        if instant > last_instant:
            silence_duration = instant - last_instant
            for i in range(silence_duration):
                events.append(('rest', last_instant + i, None))
            last_instant = instant

        max_duration = max(duration for _, duration, _ in group)
        # Divide em semifusas
        for i in range(max_duration):
            notes_in_this_instant = [parse_note_name(name) for _, duration, name in group if i < duration]
            events.append(('note', instant + i, notes_in_this_instant))
        last_instant = instant + max_duration

    # Agora monta as medidas com beams, ties e tudo mais
    ongoing_ties = {}

    for idx, (etype, time, pitches) in enumerate(events):
        if measure is None or time_in_measure >= measure_duration:
            measure = ET.SubElement(part, 'measure', number=str(measure_number))
            measure_number += 1
            attributes = ET.SubElement(measure, 'attributes')
            ET.SubElement(attributes, 'divisions').text = str(DIVISIONS)
            time_tag = ET.SubElement(attributes, 'time')
            ET.SubElement(time_tag, 'beats').text = '4'
            ET.SubElement(time_tag, 'beat-type').text = '4'
            key = ET.SubElement(attributes, 'key')
            ET.SubElement(key, 'fifths').text = '0'
            clef = ET.SubElement(attributes, 'clef')
            ET.SubElement(clef, 'sign').text = 'G'
            ET.SubElement(clef, 'line').text = '2'
            time_in_measure = 0

        # Descobre se deve ser begin / continue / end no beam
        if idx == 0 or events[idx - 1][0] != etype:
            beam = 'begin'
        elif idx == len(events) - 1 or events[idx + 1][0] != etype:
            beam = 'end'
        else:
            beam = 'continue'

        if etype == 'rest':
            measure.append(create_rest(voice=1, beam_type=beam))
        elif etype == 'note':
            first = True
            for step, alter, octave in pitches:
                tie_start = False
                tie_stop = False

                key = (step, alter, octave)
                if key in ongoing_ties:
                    tie_start = True
                
                # Verifica se continua
                future = any(
                    key in events[i][2] if events[i][0] == 'note' else False
                    for i in range(idx+1, len(events))
                )
                
                if future:
                    tie_stop = True

                if tie_start and not tie_stop:
                    ongoing_ties.pop(key)
                elif tie_stop:
                    ongoing_ties[key] = True

                measure.append(create_single_note(step, alter, octave, voice=1, is_chord=not first, tie_start=tie_start, tie_stop=tie_stop, beam_type=beam))
                first = False

        time_in_measure += 1

    tree = ET.ElementTree(score)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
