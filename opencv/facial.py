import numpy as np
import cv2

# Clasificador de reconocimiento facial // La ruta que completa es la ruta de la nueva carpeta que creó
faceCascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')

# Identifica el clasificador del ojo
eyeCascade = cv2.CascadeClassifier(r'./haarcascade_eye.xml')

# Enciende la camara
cap = cv2.VideoCapture(0)
ok = True

while ok:
    # Lea la imagen en la cámara, ok es el parámetro de juicio de si la lectura es exitosa
    ok, img = cap.read()
    # Convertir a imagen en escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detección de rostro
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(32, 32)
    )
    result = []
    # Detecta ojos según la detección de rostros
    for (x, y, w, h) in faces:
        fac_gray = gray[y: (y+h), x: (x+w)]
        result = []
        eyes = eyeCascade.detectMultiScale(fac_gray, 1.3, 2)

        # Conversión de coordenadas del ojo, cambio de posición relativa a posición absoluta
        for (ex, ey, ew, eh) in eyes:
            result.append((x+ex, y+ey, ew, eh))

    # Dibujar rectángulo
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    for (ex, ey, ew, eh) in result:
        cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
 
    cv2.imshow('video', img)

    k = cv2.waitKey(1)
    if k == 27:    # press 'ESC' to quit
        break
 
cap.release()
cv2.destroyAllWindows()
