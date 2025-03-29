from watch_video import watch_video_and_detect_color_changes
from build_keys_attributes import process_video_and_identify_balls

video_path = '../videos/heart_and_soul_cutted.webm'
balls_image_path = '../images/heart_and_soul_frame_keys_cordinates.png'
original_image_path = '../images/heart_and_soul_frame.png'
output_path = '../images/heart_and_soul_keys_identified.png'
frame_path = '../images/heart_and_soul_frame.png'

balls_info = process_video_and_identify_balls(video_path, balls_image_path, original_image_path, output_path, frame_path)
up_and_down_keys = watch_video_and_detect_color_changes(video_path, balls_info)

def calculate_notes_durations(up_and_down_keys):
    music = {}
    for key, up_and_downs in up_and_down_keys.items():
        up_and_downs_size = len(up_and_downs)
        if up_and_downs_size % 2 != 0: up_and_downs_size -= 1 # ensuring that the song doesn't end with any keys pressed
        tracks = []
        for i in range(up_and_downs_size // 2):
            track = up_and_downs[i + 1] - up_and_downs[i]
            tracks.append(track)
            i += 2
        music[key] = tracks

    return music

music = calculate_notes_durations(up_and_down_keys)

print(music)
