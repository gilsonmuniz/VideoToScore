import cv2
import numpy as np

def detectar_teclas(video_path):
    # Abrir o vídeo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Não foi possível abrir o vídeo. Verifique o arquivo.")
    
    # Obter total de frames e calcular o frame do meio
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame_idx = total_frames // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_idx)
    
    # Capturar o frame do meio
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError("Não foi possível capturar o frame do meio do vídeo.")
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar detecção de bordas
    edges = cv2.Canny(gray, 50, 150)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Lista para armazenar coordenadas centrais
    key_centers = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2
        key_centers.append((center_x, center_y))
    
    # Ordenar as teclas da esquerda para a direita
    key_centers = sorted(key_centers, key=lambda coord: coord[0])
    
    return key_centers

# Exemplo de uso
video_path = "videos/heart_and_soul.webm"
teclas = detectar_teclas(video_path)
print(teclas)
