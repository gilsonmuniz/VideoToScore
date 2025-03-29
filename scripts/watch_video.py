import cv2
import numpy as np
from build_keys_attributes import process_video_and_identify_balls
from name_keys import name_keys
from datetime import datetime
import os

COLOR_THRESHOLD = 170

def watch_video_and_detect_color_changes(video_path, balls_info):
    """
    Assista ao vídeo e detecta quando a cor de uma bola muda.
    - `video_path`: Caminho para o vídeo.
    - `balls_info`: Dicionário com informações das bolas, incluindo suas cores originais.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video not found.")
        return

    previous_colors = {ball_number: info['color'] for ball_number, info in balls_info.items()}

    keys_names, music = name_keys(11, 36), {}
    for name in keys_names.values(): music[name] = []

    while True:
        ret, frame = cap.read()

        if not ret: break # end of video

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 # to seconds

        # Para cada bola, verificar se a cor mudou
        for ball_number, info in balls_info.items():
            x, y = info['x'], info['y']
            original_color_hex = info['color']

            current_color_bgr = frame[y, x]
            current_color_rgb = np.array([current_color_bgr[2], current_color_bgr[1], current_color_bgr[0]])
            previous_color_hex = previous_colors[ball_number]
            previous_color_rgb = np.array([int(previous_color_hex[1:3], 16), int(previous_color_hex[3:5], 16), int(previous_color_hex[5:7], 16)])

            # euclidian distance
            color_distance = np.linalg.norm(current_color_rgb - previous_color_rgb)

            if color_distance > COLOR_THRESHOLD:
                key_name = keys_names[ball_number]
                music[key_name].append(current_time)
                current_color_hex = '#{:02x}{:02x}{:02x}'.format(current_color_rgb[0], current_color_rgb[1], current_color_rgb[2])
                previous_colors[ball_number] = current_color_hex

                if key_name == 'C3':
                    ret, frame = cap.read()
                    if ret:
                        # Obter o instante atual do vídeo (tempo atual do vídeo em segundos)
                        current_video_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convertendo para segundos

                        # Gerar o nome do arquivo com timestamp do vídeo e o código hexadecimal da cor
                        filename = os.path.join(
                            '../frames', 
                            f"frame_{current_video_time:.2f}s_{current_color_hex[1:]}.png"
                        )

                        cv2.imwrite(filename, frame)

    cap.release()

    return music

video_path = '../videos/heart_and_soul_cutted.webm'
balls_image_path = '../images/heart_and_soul_frame_keys_cordinates.png'
original_image_path = '../images/heart_and_soul_frame.png'
output_path = '../images/heart_and_soul_keys_identified.png'
frame_path = '../images/heart_and_soul_frame.png'

balls_info = process_video_and_identify_balls(video_path, balls_image_path, original_image_path, output_path, frame_path)
music = watch_video_and_detect_color_changes(video_path, balls_info)
