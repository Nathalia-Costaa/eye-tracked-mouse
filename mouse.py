import mediapipe as mp
import cv2
import pyautogui
import time

pyautogui.FAILSAFE = False # desativa a função de desligar o uso do olhar
sensibilidade_do_modelo = 25

# lendo a camera e incializando a solução
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# coletar o tamanho da tela
tela_w, tela_h = pyautogui.size()

# coletar especificações da camera
_, frame = cam.read()
frame_h, frame_w, _ = frame.shape

pyautogui.moveTo(0, 0)
# loop principal
while True:
    _, img = cam.read()
    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_img)
    landmark_points = results.multi_face_landmarks

    if landmark_points:
        landmarks = landmark_points[0].landmark

        iris_and_mouth = [landmarks[145], landmarks[159], landmarks[13], landmarks[14], landmarks[468]]

        distancia_da_boca = iris_and_mouth[-2].y - iris_and_mouth[-3].y

        if distancia_da_boca > 0.076:
            pass
        else:
            # codigo do mouse
            iris_principal = iris_and_mouth[0]
            # adaptar x,y para pixels
            x = (iris_and_mouth[4].x-0.32)
            y = (iris_and_mouth[4].y-0.40)
            x = int(x * frame_w) * sensibilidade_do_modelo
            y = int(y * frame_h) * sensibilidade_do_modelo
            #todo: colocar offset, olhar para um ponto e pegar a diferença
            pyautogui.moveTo(x, y)
            print(pyautogui.onScreen(x, y))

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

    # Esperando a letra q
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
