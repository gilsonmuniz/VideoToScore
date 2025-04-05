import cv2
from get_paths import read_music_name, get_video_path, get_first_frame_image_path

def get_first_video_frame(video_path, first_frame_image_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Video not found.')
        return None
    _, frame = cap.read()
    cap.release()
    cv2.imwrite(first_frame_image_path, frame)
    return frame

# music_name = read_music_name()
# video_path = get_video_path(music_name)
# first_frame_image_path = get_first_frame_image_path(music_name)
# get_first_video_frame(video_path, first_frame_image_path)
