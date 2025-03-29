import cv2

def get_first_video_frame(video_path, first_frame_image_path):
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
        cv2.imwrite(first_frame_image_path, frame)
        # print(f"Imagem salva em: {output_image_path}")

        # Retornar o frame
        return frame
    else:
        print("Erro ao ler o frame.")
        return None

    # Fechar o arquivo de vídeo
    cap.release()
