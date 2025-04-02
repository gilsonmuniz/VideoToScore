def read_music_name():
    return input('Insira o nome da música: ')

def get_video_path(music_name):
    return '../videos/' + music_name + '.webm'

def get_balls_image_path(music_name):
    return '../images/' + music_name + '_balls.png'

def get_first_frame_image_path(music_name):
    return '../images/' + music_name + '_first_frame.png'

def get_named_keys_image_path(music_name):
    return '../images/' + music_name + '_named_keys.png'
