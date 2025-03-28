import cv2
import numpy as np
from build_keys_attributes import process_video_and_identify_balls

COLOR_THRESHOLD = 200

def watch_video_and_detect_color_changes(video_path, balls_info):
    """
    Assista ao vídeo e detecta quando a cor de uma bola muda.
    - `video_path`: Caminho para o vídeo.
    - `balls_info`: Dicionário com informações das bolas, incluindo suas cores originais.
    """
    # Abrir o vídeo
    cap = cv2.VideoCapture(video_path)
    
    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return
    
    # Armazenar o estado anterior da cor de cada bola (para detectar mudanças)
    previous_colors = {ball_number: info['color'] for ball_number, info in balls_info.items()}
    
    # Começar a assistir ao vídeo frame a frame
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break  # Fim do vídeo

        # Obter o tempo atual do vídeo (em segundos)
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Converte para segundos

        # Para cada bola, verificar se a cor mudou
        for ball_number, info in balls_info.items():
            x, y = info['x'], info['y']
            original_color_hex = info['color']

            # Obter a cor atual da bola no frame (em formato BGR)
            color_bgr = frame[y, x]
            color_rgb = np.array([color_bgr[2], color_bgr[1], color_bgr[0]])  # Converter para RGB

            # Obter a cor anterior no formato RGB
            previous_color_hex = previous_colors[ball_number]
            previous_color_rgb = np.array([
                int(previous_color_hex[1:3], 16),
                int(previous_color_hex[3:5], 16),
                int(previous_color_hex[5:7], 16)
            ])

            # Calcular a distância euclidiana entre as cores
            color_distance = np.linalg.norm(color_rgb - previous_color_rgb)

            # Se a mudança for maior que o limiar, considerar uma alteração significativa
            if color_distance > COLOR_THRESHOLD:
                # Converter a cor atual para hexadecimal
                color_hex = '#{:02x}{:02x}{:02x}'.format(color_rgb[0], color_rgb[1], color_rgb[2])

                if color_hex == original_color_hex:
                    print(f'Bola {ball_number} voltou à cor original ({original_color_hex}) no tempo {current_time:.2f}s.')
                else:
                    print(f'Bola {ball_number} mudou de cor para {color_hex} no tempo {current_time:.2f}s.')

                # Atualizar a cor no dicionário de estados anteriores
                previous_colors[ball_number] = color_hex

        # Opcional: Exibir o vídeo enquanto está sendo processado (não necessário para a tarefa)
        # cv2.imshow("Video", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Liberar o vídeo
    cap.release()
    # Fechar as janelas de vídeo, se usadas
    # cv2.destroyAllWindows()

# Exemplo de uso:
video_path = '../videos/heart_and_soul_cutted.webm'
balls_image_path = '../images/heart_and_soul_frame_keys_cordinates.png'
original_image_path = '../images/heart_and_soul_frame.png'
output_path = '../images/heart_and_soul_keys_identified.png'
frame_path = '../images/heart_and_soul_frame.png'

balls_info = {1: process_video_and_identify_balls(video_path, balls_image_path, original_image_path, output_path, frame_path)[1]}
print(balls_info)

watch_video_and_detect_color_changes(video_path, balls_info)
