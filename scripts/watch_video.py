import cv2
import numpy as np
from build_keys_attributes import process_video_and_identify_balls

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
            original_color = info['color']
            
            # Obter a cor atual da bola no frame (em formato BGR)
            color_bgr = frame[y, x]
            color_hex = '#{:02x}{:02x}{:02x}'.format(color_bgr[2], color_bgr[1], color_bgr[0])

            # Verificar se a cor mudou
            if color_hex != previous_colors[ball_number]:
                if color_hex == original_color:
                    print(f'Bola {ball_number} voltou à cor original ({original_color}) no tempo {current_time:.2f}s.')
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
