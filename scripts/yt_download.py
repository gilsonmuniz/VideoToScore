import yt_dlp
import os

def download_youtube_video(url, output_name):
    output_dir = "videos"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{output_name}.webm")

    yt_opts = {
        "format": "bestvideo[ext=webm]",
        "outtmpl": output_file,
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([url])

    return output_file

if __name__ == "__main__":
    url = input("Insira o link do vídeo do YouTube: ")
    music_name = input("Insira o nome da música: ")
    download_youtube_video(url, music_name)
    print("Download concluído.")
