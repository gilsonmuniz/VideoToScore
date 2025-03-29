import cv2
import numpy as np
from name_keys import name_keys

def identify_balls(balls_image_path, original_image_path, output_path):
    # Carregar as imagens
    balls_image = cv2.imread(balls_image_path)
    original_image = cv2.imread(original_image_path)

    # Converter para o espaço de cor HSV (melhor para detectar cores)
    hsv_img = cv2.cvtColor(balls_image, cv2.COLOR_BGR2HSV)

    # Definir os limites para a cor vermelha #FF0000 em HSV
    lower_red = np.array([0, 255, 255])  # Valor mínimo para o vermelho puro
    upper_red = np.array([10, 255, 255])  # Limite superior para o vermelho puro (ajustado para tolerância mínima)

    # Criar uma máscara para detectar apenas a cor #FF0000 (vermelho puro)
    mask = cv2.inRange(hsv_img, lower_red, upper_red)

    # Encontrar os contornos das bolas vermelhas detectadas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    balls_coordinates = []  # Lista para armazenar as coordenadas das bolas (como tupla de (x, y))

    # Detectar as bolas e armazenar suas coordenadas
    for contour in contours:
        # Se o contorno for grande o suficiente para ser uma bola
        if cv2.contourArea(contour) > 100:  # Ajuste este valor se necessário
            # Obter o centro da bola (aproximação do contorno)
            (x, y), radius = cv2.minEnclosingCircle(contour)

            # Coordenadas do centro da bola
            x, y = int(x), int(y)

            # Armazenar as coordenadas da bola (não numeradas ainda)
            balls_coordinates.append((x, y))

    # Ordenar as coordenadas das bolas pela posição horizontal (x)
    balls_coordinates.sort(key=lambda coord: coord[0])

    # Numerar as bolas da esquerda para a direita
    for balls_count, (x, y) in enumerate(balls_coordinates, start=1):
        # Desenhar o número da bola na imagem original
        key_name = name_keys(11, 36)[balls_count]
        cv2.putText(original_image, key_name, (x - 15, y - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    # Salvar a imagem com os números das bolas
    cv2.imwrite(output_path, original_image)
    # print(f'Imagem salva como: {output_path}')

    # Retornar um dicionário com as coordenadas das bolas
    return {i + 1: coord for i, coord in enumerate(balls_coordinates)}
