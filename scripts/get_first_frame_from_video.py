import cv2

def get_frame_at_second_0(video_path, output_image_path):
    # Abrir o vídeo
    cap = cv2.VideoCapture(video_path)

    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return None

    # Ler o primeiro quadro (frame)
    ret, frame = cap.read()

    # Se o frame foi lido corretamente
    if ret:
        # Salvar a imagem do primeiro frame
        cv2.imwrite(output_image_path, frame)
        # print(f"Imagem salva em: {output_image_path}")

        # Retornar o frame
        return frame
    else:
        print("Erro ao ler o frame.")
        return None

    # Fechar o arquivo de vídeo
    cap.release()

# Exemplo de uso
video_path = '../videos/heart_and_soul_cutted.webm'
output_image_path = '../images/heart_and_soul_frame.png'  # Caminho para salvar a imagem
frame = get_frame_at_second_0(video_path, output_image_path)
