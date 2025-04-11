STANDARD_NOTES_VALUES = [
    1, # semifusa
    2, # fusa
    4, # semicolcheia
    8, # colcheia
    16, # semínima
    32, # mínima
    64 # semibreve
]

def format_note_duration(note_duration):
    i = 6
    while note_duration < STANDARD_NOTES_VALUES[i]: i -= 1
    note_duration_standard = (note_duration // STANDARD_NOTES_VALUES[i]) * STANDARD_NOTES_VALUES[i]
    note_duration_dotted = note_duration_standard + STANDARD_NOTES_VALUES[i - 1]
    return min(note_duration_standard, note_duration_dotted, key=lambda n: abs(n - note_duration))
