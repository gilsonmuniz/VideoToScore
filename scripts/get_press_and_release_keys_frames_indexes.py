import cv2
import numpy as np
import os
from name_keys import name_keys

COLOR_THRESHOLD = 150

def get_press_and_release_keys_frames_indexes(video_path, keys_attributes):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video not found.")
        return

    previous_colors = {ball_number: info['color'] for ball_number, info in keys_attributes.items()}

    keys_names = name_keys(11, 36)
    press_and_release_keys_frames_indexes = {}
    frame_index = 0

    while True:
        ret, frame = cap.read()

        if not ret: break # end of video

        # for each ball, check if color has changed
        for ball_number, info in keys_attributes.items():
            x, y = info['x'], info['y']
            current_color_bgr = frame[y, x]
            current_color_rgb = np.array([current_color_bgr[2], current_color_bgr[1], current_color_bgr[0]])
            previous_color_hex = previous_colors[ball_number]
            previous_color_rgb = np.array([int(previous_color_hex[1:3], 16), int(previous_color_hex[3:5], 16), int(previous_color_hex[5:7], 16)])

            # euclidean distance
            color_distance = np.linalg.norm(current_color_rgb - previous_color_rgb)

            if color_distance > COLOR_THRESHOLD:
                key_name = keys_names[ball_number]
                press_and_release_keys_frames_indexes.setdefault(key_name, []).append(frame_index)

                # update previous color
                current_color_hex = '#{:02x}{:02x}{:02x}'.format(current_color_rgb[0], current_color_rgb[1], current_color_rgb[2])
                previous_colors[ball_number] = current_color_hex

        frame_index += 1

    cap.release()

    return press_and_release_keys_frames_indexes
