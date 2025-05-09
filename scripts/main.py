from name_keys import name_keys
from get_paths import read_music_name, get_balls_image_path, get_video_path, get_first_frame_image_path, get_named_keys_image_path, get_xml_path
from get_balls_cordinates import get_balls_cordinates
from get_first_video_frame import get_first_video_frame
from get_keys_colors import get_keys_colors
from get_press_and_release_keys_frames_indexes import get_press_and_release_keys_frames_indexes
from calculate_press_and_hold_keys_durations import calculate_press_and_hold_keys_durations
from build_music import build_music
from get_press_keys_instants import get_press_keys_instants
from format_music_values import format_music_values
from build_xml import build_xml

C3_INDEX = 11
AMOUNT_OF_KEYS = 36

music_name = read_music_name()
keys_indexes_names = name_keys(C3_INDEX, AMOUNT_OF_KEYS)
video_path = get_video_path(music_name)
first_frame_image_path = get_first_frame_image_path(music_name)
first_video_frame = get_first_video_frame(video_path, first_frame_image_path)
balls_image_path = get_balls_image_path(music_name)
named_keys_image_path = get_named_keys_image_path(music_name)
keys_coordinates = get_balls_cordinates(first_frame_image_path, balls_image_path, named_keys_image_path, keys_indexes_names)
keys_attributes = get_keys_colors(keys_coordinates, first_video_frame)
press_and_release_keys_frames_indexes = get_press_and_release_keys_frames_indexes(video_path, keys_attributes, keys_indexes_names)
press_keys_instants = get_press_keys_instants(press_and_release_keys_frames_indexes)
press_and_hold_keys_durations = calculate_press_and_hold_keys_durations(press_and_release_keys_frames_indexes)
unformatted_music = build_music(press_keys_instants, press_and_hold_keys_durations)
music = format_music_values(unformatted_music)
xml_path = get_xml_path(music_name)
xml = build_xml(music, xml_path)
print('music:', music)
