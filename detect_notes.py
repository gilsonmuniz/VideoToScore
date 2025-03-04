import cv2

def detectar_mudancas(video_path, start_time=30, end_time=40):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))  
    start_frame = start_time * fps
    end_frame = end_time * fps

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    _, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("Detecção", cv2.WINDOW_NORMAL)

    num_bolinhas = 10 # Alterar no futuro p/ identificar o número de teclas que está sendo exibido
    altura_bolinhas = prev_frame.shape[0] // 2  # Metade da altura do vídeo
    espacamento = prev_frame.shape[1] // (num_bolinhas + 1)  # Espaço entre bolinhas

    for frame_idx in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Converter para BGR para desenhar as bolinhas vermelhas
        thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        
        # Desenhar bolinhas vermelhas
        for i in range(1, num_bolinhas + 1):
            x = i * espacamento
            cv2.circle(thresh_bgr, (x, altura_bolinhas), 10, (0, 0, 255), -1)
        
        cv2.imshow("Detecção", thresh_bgr)
        
        prev_gray = gray

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Teste com seu vídeo
video_path = "videos/heart_and_soul.webm"
detectar_mudancas(video_path)
