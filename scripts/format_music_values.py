from music_dicts.test_with_dots import TEST_WITH_DOTS as music

STANDARD_NOTES_VALUES = (
    1, # semifusa
    2, # fusa
    4, # semicolcheia
    8, # colcheia
    16, # semínima
    32, # mínima
    64 # semibreve
)

def get_first_note_instant(music):
    instants = []
    for note_data in music.values():
        instants.extend(note_data.get('instants', []))
    return min(instants)

def format_note_duration(note_duration):
    i = 6
    while note_duration < STANDARD_NOTES_VALUES[i]: i -= 1
    duration_standard = (note_duration // STANDARD_NOTES_VALUES[i]) * STANDARD_NOTES_VALUES[i]
    duration_dotted = duration_standard + (STANDARD_NOTES_VALUES[i - 1] if i else 0)
    closest_formatted_duration = min(duration_standard, duration_dotted, key=lambda n: abs(n - note_duration))
    return closest_formatted_duration

def format_note_instant(note_instant, first_note_instant):
    return note_instant - first_note_instant

def format_music_values(music):
    first_note_instant = get_first_note_instant(music)
    for note_data in music.values():
        note_data['durations'] = [format_note_duration(d) for d in note_data['durations']]
        note_data['instants'] = [format_note_instant(i, first_note_instant) for i in note_data['instants']]
    return music

print(format_music_values(music))
