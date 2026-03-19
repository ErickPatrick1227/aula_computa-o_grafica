import cv2
import numpy as np

img = cv2.imread("/tmp/render_cg.png")
if img is None:
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (300, 300), (200, 100, 50), -1)
    cv2.circle(img, (450, 240), 120, (50, 150, 200), -1)
    cv2.imwrite("/tmp/render_cg.png", img)

cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur_gauss = cv2.GaussianBlur(img, (15, 15), 0)
blur_median = cv2.medianBlur(img, 15)
blur_box = cv2.blur(img, (15, 15))

bordas = cv2.Canny(cinza, threshold1=50, threshold2=150)

sobel_x = cv2.Sobel(cinza, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(cinza, cv2.CV_64F, 0, 1, ksize=3)
magnitude_grad = np.sqrt(sobel_x**2 + sobel_y**2)
magnitude_grad = cv2.normalize(magnitude_grad, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

comparacao = np.hstack([
    img,
    blur_gauss,
    cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR),
    cv2.cvtColor(magnitude_grad, cv2.COLOR_GRAY2BGR)
])

cv2.imwrite("omparacao_filtros.png", comparacao)
print("Comparação salva em omparacao_filtros.png")
print(f"Imagem final: {comparacao.shape[1]}x{comparacao.shape[0]}")