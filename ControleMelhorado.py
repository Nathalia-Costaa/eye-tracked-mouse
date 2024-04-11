import math
import mediapipe as mp
import cv2
import pyautogui

pyautogui.FAILSAFE = False # desativa a função de desligar o uso do olhar
sensibilidade_do_modelo = 3.85

# lendo a camera e incializando a solução
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# coletar o tamanho da tela
tela_w, tela_h = pyautogui.size()

# coletar especificações da camera
_, frame = cam.read()
frame_h, frame_w, _ = frame.shape

RIGHT_IRIS = [474, 475, 476, 477]
LEFT_IRIS = [469, 470, 471, 472]
L_H_LEFT = [33]  # right eye right most landmark
L_H_RIGHT = [133]  # right eye left most landmark
R_H_LEFT = [362]  # left eye right most landmark
R_H_RIGHT = [263]  # left eye left most landmark

distance = int(math.sqrt((L_H_RIGHT - L_H_LEFT**2 + (R_H_RIGHT - R_H_LEFT)**2)))

# loop principal
while True:
    _, img = cam.read()
    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_img)
    landmark_points = results.multi_face_landmarks

    if landmark_points:
        landmarks = landmark_points[0].landmark
        iris_and_mouth = [landmarks[distance], landmarks[476], landmarks[13], landmarks[14]]

        distancia_da_boca = iris_and_mouth[-1].y - iris_and_mouth[-2].y

        if distancia_da_boca > 0.076:
            pass
        else:
            # codigo do mouse
            iris_principal = iris_and_mouth[0]
            # adaptar x,y para pixels
            x = int(iris_principal.x * frame_w) * sensibilidade_do_modelo
            y = int(iris_principal.y * frame_h) * sensibilidade_do_modelo
            pyautogui.moveTo(x, y)

            distancia_da_iris = iris_and_mouth[0].y - iris_and_mouth[1].y
            print(distancia_da_iris)

            if distancia_da_iris < 0.008:
                pyautogui.click()
                pyautogui.sleep(1)
            else:
                pass

        for lm in iris_and_mouth:
            x = int(lm.x * frame_w)
            y = int(lm.y * frame_h)
            cv2.circle(img, (x, y), 4, (255, 255, 0))

    cv2.imshow('Eye tracking', img)

    # Esperando a letra q
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break