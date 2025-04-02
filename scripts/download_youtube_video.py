import os
import yt_dlp

def download_youtube_video(url, output_name):
    output_dir = '../videos'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{output_name}.webm')
    yt_opts = {'format': 'bestvideo[ext=webm]', 'outtmpl': output_file}
    with yt_dlp.YoutubeDL(yt_opts) as ydl: ydl.download([url])
    return output_file

url = input('Link do vídeo do YouTube: ')
music_name = input('Nome da música: ')
download_youtube_video(url, music_name)
