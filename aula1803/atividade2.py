import cv2
import numpy as np

img = cv2.imread("render_cg.png")

if img is None:
    img = np.random.randint(0, 255, (540, 960, 3), dtype=np.uint8)
    cv2.imwrite("render_cg.png", img)
    img = cv2.imread("render_cg.png")

print(f"Shape: {img.shape}")
print(f"Dtype: {img.dtype}")
print(f"Min/Max: {img.min()}/{img.max()}")

recorte = img[100:300, 200:500]
cv2.imwrite("crop.png", recorte)

pequena = cv2.resize(img, (320, 180))
grande = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_CUBIC)
cv2.imwrite("pequena.png", pequena)

flip_h = cv2.flip(img, 1)

cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(f"Cinza shape: {cinza.shape}")
print(f"HSV shape: {hsv.shape}")

for i, canal in enumerate(['Azul (B)', 'Verde (G)', 'Vermelho (R)']):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    print(f"Canal {canal}: máx={hist.max():.0f} no valor={hist.argmax()}")