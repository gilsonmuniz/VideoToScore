import yt_dlp

def download_youtube_video(url, output_file):
    yt_opts = {
        "format": "bestvideo[ext=webm]",  # Apenas o melhor vídeo em formato webm
        "outtmpl": f"videos/{output_file}.webm",  # Nome do arquivo de saída
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Insira o link do vídeo do YouTube: ")
    music_name = input("Insira o nome da música: ")
    download_youtube_video(url, music_name)
    print("Download concluído")
