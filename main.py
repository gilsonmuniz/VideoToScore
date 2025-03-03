import os
from scripts.yt_download import download_youtube_video
from scripts.process_video import process_video
from scripts.generate_score import generate_music_xml

if __name__ == "__main__":
    url = input("Insira o link do vídeo do YouTube: ")
    music_name = input("Insira o nome da música: ")

    # Etapa 1: Baixar o vídeo
    video_path = download_youtube_video(url, music_name)

    # Etapa 2: Processar o vídeo para detectar notas
    process_video(video_path)

    # Etapa 3: Gerar a partitura
    generate_music_xml(music_name, ["C4", "D4", "E4", "F4"])

    print("Processo concluído.")
