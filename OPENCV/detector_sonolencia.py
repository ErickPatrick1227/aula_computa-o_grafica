import cv2
import time
import os
import numpy as np

# Tenta importar winsound para Windows, caso contrário usa print(\a)
try:
    import winsound
    def beep():
        winsound.Beep(1000, 500) # 1000Hz por 500ms
except ImportError:
    def beep():
        print("\a", end="", flush=True)

def detectar_sonolencia():
    # Carregar os classificadores pré-treinados do OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Iniciar a captura da webcam ou vídeo
    import sys
    fonte = sys.argv[1] if len(sys.argv) > 1 else 0
    try:
        fonte = int(fonte)
    except:
        pass
        
    cap = cv2.VideoCapture(fonte)
    
    if not cap.isOpened():
        print(f"ERRO: Não foi possível abrir a fonte: {fonte}")
        return

    # --- CONFIGURAÇÃO DE TEMPO ---
    # Você pode ajustar este valor para 2.5 ou 1.5 conforme preferir!
    ALERTA_THRESHOLD = 2.0  # Segundos com olhos fechados para disparar o alerta
    # -----------------------------

    olhos_fechados_inicio = None
    alerta_ativo = False
    tempo_fechado_atual = 0.0

    print(f"Sistema de Detecção de Sonolência v3.1 Iniciado (Tempo de Alerta: {ALERTA_THRESHOLD}s).")
    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Inverter frame horizontalmente (efeito espelho)
        frame = cv2.flip(frame, 1)
        
        # Converter para escala de cinza
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar rostos
        rostos = face_cascade.detectMultiScale(cinza, 1.1, 5)
        
        olhos_detectados_neste_frame = False

        for (x, y, w, h) in rostos:
            # Desenhar retângulo no rosto (Azul)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # ROI para os olhos (focando na metade superior do rosto)
            roi_cinza = cinza[y + int(h/5):y + int(h/2), x + int(w/10):x + int(9*w/10)]
            roi_cor = frame[y + int(h/5):y + int(h/2), x + int(w/10):x + int(9*w/10)]
            
            # Detectar olhos
            olhos = eye_cascade.detectMultiScale(roi_cinza, 1.1, 10)
            
            if len(olhos) > 0:
                olhos_detectados_neste_frame = True
                for (ex, ey, ew, eh) in olhos:
                    # Desenhar retângulo nos olhos (Verde)
                    cv2.rectangle(roi_cor, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Lógica de Sonolência com Contador Visível
        if len(rostos) > 0:
            if not olhos_detectados_neste_frame:
                if olhos_fechados_inicio is None:
                    olhos_fechados_inicio = time.time()
                
                tempo_fechado_atual = time.time() - olhos_fechados_inicio
                
                if tempo_fechado_atual >= ALERTA_THRESHOLD:
                    alerta_ativo = True
            else:
                # Olhos detectados, reseta tudo
                olhos_fechados_inicio = None
                alerta_ativo = False
                tempo_fechado_atual = 0.0
        else:
            # Rosto não detectado, reseta para evitar erros
            olhos_fechados_inicio = None
            alerta_ativo = False
            tempo_fechado_atual = 0.0

        # --- EXIBIÇÃO NA TELA ---
        
        # 1. Barra de progresso de sonolência
        progresso = min(tempo_fechado_atual / ALERTA_THRESHOLD, 1.0)
        largura_barra = int(progresso * 300)
        cv2.rectangle(frame, (10, 60), (310, 80), (255, 255, 255), 2) # Contorno
        if progresso > 0:
            cor_barra = (0, 255, 255) if progresso < 0.8 else (0, 0, 255)
            cv2.rectangle(frame, (10, 60), (10 + largura_barra, 80), cor_barra, -1) # Preenchimento

        # 2. Texto de Status e Tempo
        status_text = "OLHOS ABERTOS" if olhos_detectados_neste_frame else "OLHOS FECHADOS"
        cor_status = (0, 255, 0) if olhos_detectados_neste_frame else (0, 0, 255)
        cv2.putText(frame, f"{status_text} ({tempo_fechado_atual:.1f}s / {ALERTA_THRESHOLD}s)", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_status, 2)

        # 3. Alerta de Sonolência
        if alerta_ativo:
            # Texto Gigante
            cv2.putText(frame, "ACORDA MOTORISTA!", (50, 200),
                        cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), 4)
            
            # Borda vermelha piscante intensa
            if int(time.time() * 10) % 2 == 0:
                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 30)
                beep() # Tenta fazer o som

        # Mostrar o vídeo
        cv2.imshow('Detector de Sonolencia v3.1', frame)

        # Sair com a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detectar_sonolencia()
