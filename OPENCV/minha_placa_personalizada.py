import os
import cv2
from placas_utils import criar_placa_sintetica, SAIDA_DIR

meu_texto = "ERI5K26" 

PLACA_PATH = criar_placa_sintetica(texto=meu_texto, largura=500, altura=150)

caminho_arquivo = os.path.join(SAIDA_DIR, "minha_placa_personalizada.png")
cv2.imwrite(caminho_arquivo, PLACA_PATH)

print(f"--- SUCESSO! ---")
