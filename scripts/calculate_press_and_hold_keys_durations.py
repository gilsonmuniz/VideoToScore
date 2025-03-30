def calculate_press_and_hold_keys_durations(press_and_release_keys_instants):
    notes_durations = {}
    for key, up_and_downs in press_and_release_keys_instants.items():
        up_and_downs_size = len(up_and_downs)
        if up_and_downs_size % 2 != 0: up_and_downs_size -= 1 # ensuring that the song doesn't end with any keys pressed
        tracks = []
        for i in range(0, up_and_downs_size, 2):
            track = up_and_downs[i + 1] - up_and_downs[i]
            tracks.append(track)
        notes_durations[key] = tracks

    return notes_durations
