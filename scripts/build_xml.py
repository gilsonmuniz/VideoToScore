import math
from functools import reduce

HEART_AND_SOUL = {
    'C3': {
        'instants': [30, 150, 270, 389, 509, 630, 749, 870, 930, 1470, 1590, 1710, 1950],
        'durations': [28, 24, 28, 22, 24, 26, 29, 18, 64, 23, 23, 22]
    },
    'C4': {
        'instants': [30, 45, 60, 99, 129, 234, 299, 389, 509, 524, 540, 580, 610, 715, 780, 870, 945, 1139, 1380, 1470, 1485, 1500, 1540, 1570, 1675, 1740, 1920, 1950],
        'durations': [7, 7, 31, 6, 7, 7, 32, 21, 10, 6, 28, 4, 5, 5, 38, 18, 43, 31, 28, 8, 4, 17, 6, 5, 5, 32, 14]
    },
    'A2': {
        'instants': [60, 194, 299, 420, 540, 780, 1050, 1500, 1620, 1740],
        'durations': [30, 12, 30, 28, 14, 29, 19, 18, 14, 28]
    },
    'F2': {
        'instants': [89, 210, 570, 689, 899, 1530, 1650, 1920],
        'durations': [27, 25, 22, 24, 18, 22, 21, 29]
    },
    'B3': {
        'instants': [104, 119, 585, 600, 1109, 1200, 1350, 1440, 1545, 1560, 1935],
        'durations': [10, 9, 8, 9, 30, 11, 31, 31, 8, 9, 14]
    },
    'A3': {
        'instants': [115, 594, 1170, 1410, 1555],
        'durations': [6, 6, 17, 28, 4]
    },
    'G2': {
        'instants': [119, 239, 366, 480, 600, 839, 1560, 1680],
        'durations': [30, 31, 24, 30, 28, 25, 30, 17]
    },
    'D4': {
        'instants': [135, 225, 239, 375, 429, 480, 615, 705, 720, 855, 910, 1044, 1080, 1285, 1320, 1575, 1665, 1680, 1815, 1915],
        'durations': [7, 8, 12, 14, 6, 29, 9, 8, 9, 15, 5, 8, 30, 5, 30, 16, 7, 10, 10, 5]
    },
    'E4': {
        'instants': [150, 164, 179, 219, 249, 359, 435, 475, 630, 645, 659, 700, 729, 839, 915, 1020, 1260, 1590, 1605, 1620, 1660, 1690, 1800, 1830, 1905],
        'durations': [8, 7, 30, 5, 4, 16, 7, 4, 8, 5, 17, 5, 5, 15, 8, 22, 24, 8, 4, 12, 5, 5, 14, 71, 8]
    },
    'F4': {
        'instants': [255, 355, 444, 464, 734, 835, 925, 1015, 1255, 1695, 1795, 1900],
        'durations': [5, 5, 5, 10, 14, 5, 7, 5, 4, 15, 4, 6]
    },
    'G4': {
        'instants': [270, 345, 449, 749, 824, 930, 1005, 1245, 1710, 1785],
        'durations': [29, 10, 16, 30, 10, 14, 9, 8, 30, 9]
    },
    'D3': {
        'instants': [330, 449, 810, 1200, 1440, 1770, 1890],
        'durations': [25, 28, 24, 11, 16, 14, 23]
    },
    'A4': {
        'instants': [340, 820, 1000, 1240, 1780],
        'durations': [4, 5, 6, 5, 5]
    },
    'F3': {
        'instants': [990, 1230],
        'durations': [20, 10]
    },
    'E3': {
        'instants': [1020, 1139, 1260, 1380, 1830],
        'durations': [16, 18, 14, 19, 16]
    },
    'F#3': {
        'instants': [1080, 1320],
        'durations': [15, 30]
    },
    'G3': {
        'instants': [1109, 1350, 1800],
        'durations': [16, 29, 17]
    },
    'D#3': {
        'instants': [1170, 1410],
        'durations': [12, 15]
    }
}

MARRIED_LIFE = {
    'C3': {
        'instants': [109, 160, 263, 314, 417, 469, 1137, 2217, 2294, 2346, 2680, 2886, 3606, 4686, 4763, 4814, 5149, 5354],
        'durations': [38, 39, 38, 39, 39, 38, 103, 52, 26, 25, 64, 38, 77, 51, 26, 26, 64, 39]
    },
    'F3': {
        'instants': [597, 649, 906, 1086, 1549, 1831, 1883, 3066, 3117, 3374, 3554, 4017, 4300, 4351, 5611],
        'durations': [26, 25, 25, 25, 38, 26, 26, 25, 26, 26, 26, 39, 26, 26, 155]
    },
    'A3': {
        'instants': [623, 931, 1291, 1446, 3091, 3400, 3760, 3914],
        'durations': [26, 26, 39, 38, 26, 26, 39, 39]
    },
    'E3': {
        'instants': [674, 957, 1909, 2140, 2191, 2320, 2783, 2989, 3143, 3426, 4377, 4609, 4660, 4789, 5251, 5457],
        'durations': [155, 26, 154, 26, 26, 26, 51, 51, 103, 25, 154, 25, 26, 25, 52, 103]
    },
    'D3': {
        'instants': [983, 1060, 1111, 1266, 1420, 1600, 1754, 2474, 2757, 2937, 3451, 3529, 3580, 3709, 3889, 4069, 4223, 4943, 5226, 5406],
        'durations': [51, 26, 26, 25, 26, 129, 52, 26, 26, 39, 52, 25, 26, 38, 25, 128, 51, 26, 25, 38]
    },
    'G3': {
        'instants': [1343, 1497, 1857, 2166, 3811, 3966, 4326, 4634],
        'durations': [38, 39, 26, 25, 65, 38, 25, 26]
    },
    'A#2': {
        'instants': [2371, 2449, 2500, 2629, 4840, 4917, 4969, 5097],
        'durations': [52, 25, 26, 38, 51, 26, 25, 39]
    },
    'A2': {
        'instants': [2577, 5046],
        'durations': [39, 38]
    }
}

TEST = {
    'C3': {
        'instants': [29],
        'durations': [1]
    },
    'D3': {
        'instants': [88],
        'durations': [2]
    },
    'E3': {
        'instants': [148],
        'durations': [3]
    },
    'F3': {
        'instants': [207],
        'durations': [6]
    },
    'G3': {
        'instants': [264],
        'durations': [14]
    },
    'A3': {
        'instants': [321],
        'durations': [30]
    },
    'B3': {
        'instants': [379],
        'durations': [58]
    }
}

def normalize_note_value(note_duration, minimum_note_duration):
    return note_duration / minimum_note_duration

def map_occurrences_of_durations(music, maximum_note_duration):
    occurrence_map = []
    for _ in range(maximum_note_duration + 1): occurrence_map.append(0)
    for instants_and_durations in music.values():
        for duration in instants_and_durations['durations']:
            occurrence_map[duration] += 1
    return occurrence_map

minimum_note_duration = min(d for note in MARRIED_LIFE.values() for d in note["durations"])
maximum_note_duration = max(d for note in MARRIED_LIFE.values() for d in note["durations"])

durations = MARRIED_LIFE['E3']['durations']

print(durations)
print('Max:', maximum_note_duration)
print('Min:', minimum_note_duration)
print(map_occurrences_of_durations(MARRIED_LIFE, maximum_note_duration))

for duration in durations:
    print(normalize_note_value(duration, minimum_note_duration), end=' ')
print()
