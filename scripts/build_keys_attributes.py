from get_first_frame_from_video import get_frame_at_second_0
from detect_balls import identify_balls
import cv2

def process_video_and_identify_balls(video_path, balls_image_path, original_image_path, output_path, frame_path):
    # 1. Chamar a função get_frame_at_second_0
    # Isso deve retornar o caminho do frame salvo ou o próprio frame.
    get_frame_at_second_0(video_path, frame_path)
    
    # 2. Chamar a função identify_balls
    # Isso vai retornar o dicionário com as coordenadas das bolas
    balls_coordinates = identify_balls(balls_image_path, original_image_path, output_path)
    
    # 3. Carregar o frame salvo pela função get_frame_at_second_0
    frame = cv2.imread(frame_path)

    # 4. Para cada bola, adicionar a chave 'color' com a cor no dicionário de bolas
    for ball_number, (x, y) in balls_coordinates.items():
        # Obter a cor da imagem no ponto (x, y)
        color_bgr = frame[y, x]
        # Converter para formato hexadecimal
        color_hex = '#{:02x}{:02x}{:02x}'.format(color_bgr[2], color_bgr[1], color_bgr[0])
        
        # Adicionar a cor no dicionário de bolas
        balls_coordinates[ball_number] = {'x': x, 'y': y, 'color': color_hex}

    # 5. Retornar o dicionário atualizado com as cores
    return balls_coordinates

# Exemplo de uso:
video_path = '../videos/heart_and_soul_cutted.webm'
balls_image_path = '../images/heart_and_soul_frame_keys_cordinates.png'
original_image_path = '../images/heart_and_soul_frame.png'
output_path = '../images/heart_and_soul_keys_identified.png'
frame_path = '../images/test.png'

balls_info = process_video_and_identify_balls(video_path, balls_image_path, original_image_path, output_path, frame_path)

# Exibir os resultados no terminal
for ball_number, info in balls_info.items():
    print(f'Bola {ball_number}:')
    print(f'    x={info["x"]}, y={info["y"]}, color={info["color"]}')
