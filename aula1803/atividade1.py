import cv2
import numpy as np

img = np.zeros((480, 640, 3), dtype=np.uint8)
print(f"Shape: {img.shape}")

img[0:240, 0:320] = (255, 0, 0)
img[0:240, 320:640] = (0, 255, 0)
img[240:480, 0:320] = (0, 0, 255)
img[240:480, 320:640] = (128, 128, 128)

cv2.circle(img, (320, 240), 80, (255, 255, 0), thickness=3)
cv2.rectangle(img, (100, 100), (250, 200), (255, 255, 255), thickness=2)
cv2.line(img, (0, 0), (640, 480), (0, 255, 255), thickness=2)

cv2.putText(
    img, "Computacao Grafica - UNIFG",
    (160, 460), cv2.FONT_HERSHEY_SIMPLEX,
    0.8, (255, 255, 255), 2
)

cv2.imwrite("aula09_basico.png", img)
print("Salva em aula09_basico.png")

cv2.imshow("Imagem", img)
cv2.waitKey(0)
cv2.destroyAllWindows()