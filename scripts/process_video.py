import cv2
import os
import numpy as np

def detect_notes(video_path):    
    cap = cv2.VideoCapture(video_path)
    
    print(f"Processando vídeo: {video_path}")
    
    notes_detected = []
    prev_frame = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        roi = gray[int(height * 0.4):int(height * 0.6), :]
        
        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, roi)
            _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
            if np.sum(thresh) > 10000:
                notes_detected.append("C4")  # Exemplo: associar notas reais depois
        
        prev_frame = roi
    
    cap.release()
    return notes_detected

if __name__ == "__main__":
    video_name = input("Insira o nome do vídeo (sem extensão): ")
    video_path = os.path.join("videos", f"{video_name}.webm")
    detected_notes = detect_notes(video_path)
    print("Notas detectadas:", detected_notes)
