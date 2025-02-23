import subprocess

# Solicita a URL do usuário
video_url = input("Digite a URL do vídeo do YouTube: ")

# Nome da Música
music_name = input("Digite o nome da música: ")

# Comando yt-dlp para baixar e converter para WAV
command = f'yt-dlp -f "bestaudio" -x --audio-format wav -o "audios/{music_name}" "{video_url}"'

# Executa o comando no terminal
subprocess.run(command, shell=True, check=True)

print("\nÁudio foi salvo como '{}".format(music_name))
