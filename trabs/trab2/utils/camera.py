import cv2

class CameraManager:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError("Não foi possível acessar a câmera.")

    def get_frame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()