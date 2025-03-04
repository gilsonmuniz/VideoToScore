import os
from scripts.yt_download import download_youtube_video
from scripts.process_video import detect_notes
from scripts.generate_score import generate_music_xml

if __name__ == "__main__":
    music_name = input("Insira o nome da música: ")
    video_path = os.path.join("videos", f"{music_name}.webm")

    # Etapa 1: Baixar o vídeo (caso não esteja baixado ainda)
    if not os.path.exists(video_path):
        url = input("Insira o link do vídeo do YouTube: ")
        video_path = download_youtube_video(url, music_name)
    else:
        print(f"O vídeo '{music_name}' já existe. Pulando o download.")

    # Etapa 2: Processar o vídeo para detectar notas
    detected_notes = detect_notes(video_path)  # Agora retorna as notas detectadas
    print(detected_notes)

    # Etapa 3: Gerar a partitura com as notas extraídas
    generate_music_xml(music_name, detected_notes)

    print("Processo concluído.")
