NOTES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

def name_keys(c3_index, number_of_keys):
    keyboard = {}
    octave_index = 3
    note_position = 0
    for note_index in range(c3_index, -1, -1):
        key_name = NOTES[note_position] + str(octave_index)
        keyboard[note_index] = key_name
        note_position -= 1
        if note_position <= 0:
            note_position = 11
            octave_index -= 1
    octave_index = 3
    note_position = 0
    for note_index in range(c3_index, number_of_keys + 1):
        key_name = NOTES[note_position] + str(octave_index)
        keyboard[note_index] = key_name
        note_position += 1
        if note_position >= 12:
            note_position = 0
            octave_index += 1

    return keyboard

# name_keys(11, 13)
