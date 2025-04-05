import cv2

def get_first_video_frame(video_path, first_frame_image_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Video not found.')
        return None
    _, frame = cap.read()
    cap.release()
    cv2.imwrite(first_frame_image_path, frame)
    return frame
