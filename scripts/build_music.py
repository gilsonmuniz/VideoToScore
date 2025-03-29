def build_music(press_keys_instants, press_and_hold_keys_durations):
    music = {}
    for key in press_keys_instants.keys():
        music[key] = {'instants': press_keys_instants[key],
                      'durations': press_and_hold_keys_durations[key]}
    return music
