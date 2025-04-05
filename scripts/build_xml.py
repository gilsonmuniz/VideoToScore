from music_dicts.test import TEST as music

def normalize_note_value(note_duration, minimum_note_duration):
    return note_duration / minimum_note_duration

def map_occurrences_of_durations(music, maximum_note_duration):
    occurrence_map = []
    for _ in range(maximum_note_duration + 1): occurrence_map.append(0)
    for instants_and_durations in music.values():
        for duration in instants_and_durations['durations']:
            occurrence_map[duration] += 1
    return occurrence_map

minimum_note_duration = min(d for note in music.values() for d in note['durations'])
maximum_note_duration = max(d for note in music.values() for d in note['durations'])

durations = music['E3']['durations']

print(durations)
print('Max:', maximum_note_duration)
print('Min:', minimum_note_duration)
print(map_occurrences_of_durations(music, maximum_note_duration))

for duration in durations:
    print(normalize_note_value(duration, minimum_note_duration), end=' ')
print()
