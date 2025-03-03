import cv2
import os

def process_video(video_path):
    if not os.path.exists(video_path):
        print(f"Erro: Arquivo {video_path} não encontrado.")
        return
    
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return
    
    # Processamento de vídeo para detectar notas (lógica a ser implementada)
    print(f"Processando vídeo: {video_path}")

    cap.release()

if __name__ == "__main__":
    video_name = input("Insira o nome do vídeo (sem extensão): ")
    video_path = os.path.join("videos", f"{video_name}.webm")
    process_video(video_path)
