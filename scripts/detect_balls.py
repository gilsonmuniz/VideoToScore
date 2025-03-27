import cv2
import numpy as np

def identify_balls(balls_image_path, original_image_path, output_path):
    # Carregar as imagens
    balls_image = cv2.imread(balls_image_path)
    original_image = cv2.imread(original_image_path)

    # Converter para o espaço de cor HSV (melhor para detectar cores)
    hsv_img = cv2.cvtColor(balls_image, cv2.COLOR_BGR2HSV)

    # Definir os limites para a cor vermelha #FF0000 em HSV
    # #FF0000 é equivalente a (0, 255, 255) em HSV (vermelho puro)
    lower_red = np.array([0, 255, 255])  # Valor mínimo para o vermelho puro
    upper_red = np.array([10, 255, 255])  # Limite superior para o vermelho puro (ajustado para tolerância mínima)

    # Criar uma máscara para detectar apenas a cor #FF0000 (vermelho puro)
    mask = cv2.inRange(hsv_img, lower_red, upper_red)

    # Encontrar os contornos das bolas vermelhas detectadas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    balls_count = 1
    balls_coordinates = {}  # Dicionário para armazenar as coordenadas das bolas

    for contour in contours:
        # Se o contorno for grande o suficiente para ser uma bola
        if cv2.contourArea(contour) > 100:  # Ajuste este valor se necessário
            # Obter o centro da bola (aproximação do contorno)
            (x, y), radius = cv2.minEnclosingCircle(contour)

            # Coordenadas do centro da bola
            x, y = int(x), int(y)

            # Obter a cor da imagem original nesse ponto
            original_color = original_image[y, x]
            cor_hex = '#{:02x}{:02x}{:02x}'.format(original_color[2], original_color[1], original_color[0])

            # Armazenar as coordenadas no dicionário
            balls_coordinates[balls_count] = (x, y)

            cv2.putText(original_image, str(balls_count), (x - 15, y - 15), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)


            balls_count += 1

    # Salvar a imagem com os "X"s azuis
    cv2.imwrite(output_path, original_image)
    print(f'Imagem salva como: {output_path}')

    # Retornar o dicionário com as coordenadas das bolas
    return balls_coordinates
