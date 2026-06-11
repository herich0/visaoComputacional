import cv2
import pygame

class OcarinaVirtual:
    def __init__(self, audio_paths, ref_id=0, hole_ids=(1, 2, 3, 4)):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)
        self.ref_id = ref_id
        self.hole_ids = list(hole_ids)
        
        pygame.mixer.init()
        self.sounds = {h_id: pygame.mixer.Sound(path) for h_id, path in zip(self.hole_ids, audio_paths)}
        
        for sound in self.sounds.values():
            sound.set_volume(0.25)
            
        self.playing = {h_id: False for h_id in self.hole_ids}

    def process_frame(self, frame):
        corners, ids, _ = self.detector.detectMarkers(frame)
        
        detected_ids = []
        if ids is not None:
            detected_ids = [i[0] for i in ids]
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            if self.ref_id in detected_ids:
                idx = detected_ids.index(self.ref_id)
                ref_center = corners[idx][0].mean(axis=0)
                cv2.putText(frame, "Ocarina Base", (int(ref_center[0]), int(ref_center[1])-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        for h_id in self.hole_ids:
            if h_id not in detected_ids and (self.ref_id in detected_ids):
                if not self.playing[h_id]:
                    self.sounds[h_id].play(-1)
                    self.playing[h_id] = True
            else:
                if self.playing[h_id]:
                    self.sounds[h_id].stop()
                    self.playing[h_id] = False
                    
        return frame