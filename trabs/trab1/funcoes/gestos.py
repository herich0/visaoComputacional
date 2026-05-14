import cv2
import numpy as np
import pyautogui

class ControladorGestos:
    def __init__(self):
        # Parâmetros do Lucas-Kanade
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # Parâmetros para achar os pontos iniciais da mão
        self.feature_params = dict(maxCorners=1, qualityLevel=0.3, minDistance=7, blockSize=7)
        
        self.old_gray = None
        self.p0 = None
        self.cooldown = 0 

    def processar_frame(self, frame):
        # Inverte como um espelho para ficar intuitivo
        frame = cv2.flip(frame, 1)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.cooldown > 0:
            self.cooldown -= 1

        # Se não tem ponto sendo rastreado, tenta encontrar um no centro da tela
        if self.p0 is None:
            altura, largura = frame_gray.shape
            # Pega uma "caixa" no centro da tela para procurar a mão
            roi = frame_gray[int(altura*0.2):int(altura*0.8), int(largura*0.2):int(largura*0.8)]
            pontos = cv2.goodFeaturesToTrack(roi, mask=None, **self.feature_params)
            
            if pontos is not None:
                # Ajusta as coordenadas da ROI para a tela inteira
                for p in pontos:
                    p[0][0] += int(largura*0.2)
                    p[0][1] += int(altura*0.2)
                self.p0 = pontos
                self.old_gray = frame_gray.copy()
            
            # Desenha um retângulo mostrando onde colocar a mão
            cv2.rectangle(frame, (int(largura*0.2), int(altura*0.2)), (int(largura*0.8), int(altura*0.8)), (255, 0, 0), 2)
            cv2.putText(frame, "Coloque a mao no quadrado", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
            return frame

        # Calcula o fluxo óptico
        p1, st, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray, self.p0, None, **self.lk_params)

        # Se encontrou o ponto no novo frame
        if p1 is not None and st[0][0] == 1:
            novo_ponto = p1[0][0]
            ponto_antigo = self.p0[0][0]
            
            # Calcula a diferença no eixo X
            dx = novo_ponto[0] - ponto_antigo[0]
            
            if self.cooldown == 0:
                if dx > 60: # Gesto rápido para a direita
                    pyautogui.press('right')
                    print("Slide -> Avançar")
                    self.cooldown = 30 # Pausa os cálculos por 30 frames
                    self.p0 = None # Reseta o ponto para achar a mão parada de novo
                elif dx < -60: # Gesto rápido para a esquerda
                    pyautogui.press('left')
                    print("Slide <- Retroceder")
                    self.cooldown = 30
                    self.p0 = None
                else:
                    self.p0 = p1[st == 1].reshape(-1, 1, 2)
            else:
                 self.p0 = p1[st == 1].reshape(-1, 1, 2)
                 cv2.putText(frame, "Aguarde...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                 
            # Desenha uma bolinha verde onde está rastreando
            cv2.circle(frame, (int(novo_ponto[0]), int(novo_ponto[1])), 10, (0, 255, 0), -1)
        else:
            self.p0 = None # Perdeu o rastreio, vai procurar de novo

        self.old_gray = frame_gray.copy()
        return frame