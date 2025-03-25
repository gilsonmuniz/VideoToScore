import cv2
import numpy as np

def identificar_bolas(imagem_com_bolas, imagem_original, output_path):
    # Carregar as imagens
    img_bolas = cv2.imread(imagem_com_bolas)
    img_original = cv2.imread(imagem_original)

    # Converter para o espaço de cor HSV (melhor para detectar cores)
    hsv_img = cv2.cvtColor(img_bolas, cv2.COLOR_BGR2HSV)

    # Definir os limites para a cor vermelha #FF0000 em HSV
    # #FF0000 é equivalente a (0, 255, 255) em HSV (vermelho puro)
    lower_red = np.array([0, 255, 255])  # Valor mínimo para o vermelho puro
    upper_red = np.array([10, 255, 255])  # Limite superior para o vermelho puro (ajustado para tolerância mínima)

    # Criar uma máscara para detectar apenas a cor #FF0000 (vermelho puro)
    mask = cv2.inRange(hsv_img, lower_red, upper_red)

    # Encontrar os contornos das bolas vermelhas detectadas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bola_count = 1
    for contour in contours:
        # Se o contorno for grande o suficiente para ser uma bola
        if cv2.contourArea(contour) > 100:  # Ajuste este valor se necessário
            # Obter o centro da bola (aproximação do contorno)
            (x, y), radius = cv2.minEnclosingCircle(contour)

            # Coordenadas do centro da bola
            x, y = int(x), int(y)

            # Obter a cor da imagem original nesse ponto
            cor_original = img_original[y, x]
            cor_hex = '#{:02x}{:02x}{:02x}'.format(cor_original[2], cor_original[1], cor_original[0])

            # Imprimir as informações
            print(f'Bola {bola_count}:')
            print(f'    Posição: x={x}, y={y}')
            print(f'    Cor da imagem original nesse ponto: {cor_hex}')
            print()

            # Desenhar um "X" azul na imagem original
            cv2.line(img_original, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)  # Linha diagonal 1
            cv2.line(img_original, (x - 10, y + 10), (x + 10, y - 10), (255, 0, 0), 2)  # Linha diagonal 2

            bola_count += 1

    # Salvar a imagem com os "X"s azuis
    cv2.imwrite(output_path, img_original)
    print(f'Imagem salva como: {output_path}')

# Exemplo de uso
imagem_com_bolas = '../images/heart_and_soul_frame_keys_cordinates.png'
imagem_original = '../images/heart_and_soul_frame.png'
output_path = '../images/imagem_com_Xs_azuis.png'
identificar_bolas(imagem_com_bolas, imagem_original, output_path)
