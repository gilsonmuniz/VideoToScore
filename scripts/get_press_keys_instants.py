def get_press_keys_instants(press_and_release_keys_instants):
    press_keys_instants = {}
    print('press_and_release_keys_instants:', press_and_release_keys_instants)
    for key, instants in press_and_release_keys_instants.items():
        print('key:', key)
        print('instants:', instants)
        interactions = len(instants)
        press_key_instants = []
        if interactions:
            for i in range(0, interactions, 2): press_key_instants.append(instants[i])
    return press_keys_instants