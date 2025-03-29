import cv2

def get_keys_colors(keys_coordinates, first_video_frame):
    for ball_index, (x, y) in keys_coordinates.items():
        color_bgr = first_video_frame[y, x]
        color_hex = '#{:02x}{:02x}{:02x}'.format(color_bgr[2], color_bgr[1], color_bgr[0])
        keys_coordinates[ball_index] = {'x': x, 'y': y, 'color': color_hex}

    return keys_coordinates
