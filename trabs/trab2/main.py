import cv2
from utils.camera import CameraManager
from modulos.metrologia import MetrologiaArUco
from modulos.ocarina import OcarinaVirtual
from modulos.vr_hand import VRHand

def main():
    cam = CameraManager(0)
    
    metrologia = MetrologiaArUco(marker_size_cm=5.0)
    ocarina = OcarinaVirtual(['assets/audios/som1.wav', 'assets/audios/som2.wav', 
                              'assets/audios/som3.wav', 'assets/audios/som4.wav'])
    vr = VRHand(['assets/audios/som1.wav', 'assets/audios/som2.wav', 
                 'assets/audios/som3.wav', 'assets/audios/som4.wav'])
    
    modo_atual = 'nenhum'
    espelhar = False

    while True:
        ret, frame = cam.get_frame()
        if not ret:
            break

        if modo_atual == 'metrologia':
            frame = metrologia.process_frame(frame)
        elif modo_atual == 'ocarina':
            frame = ocarina.process_frame(frame)
        elif modo_atual == 'vr':
            frame = vr.process_frame(frame)

        if espelhar:
            frame = cv2.flip(frame, 1)

        menu_text = "Pressione: [1] Metrologia | [2] Ocarina | [3] VR | [Q] Sair | [S] Espelhar"
        cv2.putText(frame, menu_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        status_text = f"Modo Atual: {modo_atual.upper()}"
        cv2.putText(frame, status_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("TP2 - Visao Computacional", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('1'):
            modo_atual = 'metrologia'
        elif key == ord('2'):
            modo_atual = 'ocarina'
        elif key == ord('3'):
            modo_atual = 'vr'
        elif key == ord('s'):
            espelhar = not espelhar
        elif key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()