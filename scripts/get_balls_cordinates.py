import cv2
import numpy as np

def get_balls_cordinates(first_frame_image_path, balls_image_path, named_keys_image_path, keys_indexes_names):
    first_frame_image = cv2.imread(first_frame_image_path)
    balls_image = cv2.imread(balls_image_path)

    # Converter para o espaço de cor HSV (melhor para detectar cores)
    hsv_img = cv2.cvtColor(balls_image, cv2.COLOR_BGR2HSV)

    # tolerance for red color
    lower_red = np.array([0, 255, 255])
    upper_red = np.array([10, 255, 255])

    # mask to detect only red color, balls color
    mask = cv2.inRange(hsv_img, lower_red, upper_red)

    # find the red balls contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    balls_coordinates = []

    # Detectar as bolas e armazenar suas coordenadas
    for contour in contours:
        # Se o contorno for grande o suficiente para ser uma bola
        if cv2.contourArea(contour) > 100:  # Ajuste este valor se necessário
            # Obter o centro da bola (aproximação do contorno)
            (x, y), _ = cv2.minEnclosingCircle(contour)

            # ball center
            x, y = int(x), int(y)

            # Armazenar as coordenadas da bola (não numeradas ainda)
            balls_coordinates.append((x, y))

    # enumerate balls from left to right
    balls_coordinates.sort(key=lambda coord: coord[0])
    for balls_count, (x, y) in enumerate(balls_coordinates, start=1):
        # write notes names in keys
        key_name = keys_indexes_names[balls_count]
        cv2.putText(first_frame_image, key_name, (x - 15, y - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    # save keys_identified_image
    cv2.imwrite(named_keys_image_path, first_frame_image)

    # dict of balls cordinates
    return {i + 1: coord for i, coord in enumerate(balls_coordinates)}
