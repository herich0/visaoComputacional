import cv2
import numpy as np
import math
import pygame
import mediapipe as mp

class VRHand:
    def __init__(self, audio_paths):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, 
            max_num_hands=2, 
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        pygame.mixer.init()
        self.sounds = [pygame.mixer.Sound(path) for path in audio_paths]
        
        for sound in self.sounds:
            sound.set_volume(0.25)
            
        self.playing = [False] * 4

        self.tip_ids = [
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]

        self.modo_cubo = True
        self.dedoes_tocando = False

    def desenhar_cubo(self, frame, cx, cy, size=30):
        offset = int(size * 0.5)
        
        pts_front = np.array([
            [cx - size, cy - size], [cx + size, cy - size],
            [cx + size, cy + size], [cx - size, cy + size]
        ], np.int32)
        
        pts_back = np.array([
            [cx - size + offset, cy - size - offset], [cx + size + offset, cy - size - offset],
            [cx + size + offset, cy + size - offset], [cx - size + offset, cy + size - offset]
        ], np.int32)

        cv2.polylines(frame, [pts_front], True, (255, 0, 255), 2)
        cv2.polylines(frame, [pts_back], True, (0, 255, 255), 2)
        
        for i in range(4):
            cv2.line(frame, tuple(pts_front[i]), tuple(pts_back[i]), (255, 255, 0), 2)

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        active_touches = [False] * 4

        if results.multi_hand_landmarks:
            h, w, _ = frame.shape
            
            if len(results.multi_hand_landmarks) == 2:
                hand1 = results.multi_hand_landmarks[0]
                hand2 = results.multi_hand_landmarks[1]
                
                th1 = hand1.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                th2 = hand2.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                
                tx1, ty1 = int(th1.x * w), int(th1.y * h)
                tx2, ty2 = int(th2.x * w), int(th2.y * h)
                
                dist_th = math.dist((tx1, ty1), (tx2, ty2))
                
                dedoes_agora = dist_th < 30
                if dedoes_agora and not self.dedoes_tocando:
                    self.modo_cubo = not self.modo_cubo
                self.dedoes_tocando = dedoes_agora
                
                if not self.modo_cubo:
                    for i, tip_id in enumerate(self.tip_ids):
                        lm1 = hand1.landmark[tip_id]
                        lm2 = hand2.landmark[tip_id]
                        
                        lx1, ly1 = int(lm1.x * w), int(lm1.y * h)
                        lx2, ly2 = int(lm2.x * w), int(lm2.y * h)
                        
                        dist = math.dist((lx1, ly1), (lx2, ly2))
                        
                        if dist < 30:
                            active_touches[i] = True
                            cv2.circle(frame, (int((lx1+lx2)/2), int((ly1+ly2)/2)), 15, (0, 0, 255), cv2.FILLED)

            else:
                self.dedoes_tocando = False

            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                if self.modo_cubo:
                    pt4 = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    pt8 = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    
                    tx4, ty4 = int(pt4.x * w), int(pt4.y * h)
                    tx8, ty8 = int(pt8.x * w), int(pt8.y * h)
                    
                    cx = int((tx4 + tx8) / 2)
                    cy = int((ty4 + ty8) / 2)
                    
                    size = int(math.dist((tx4, ty4), (tx8, ty8)) / 2)
                    if size < 5:
                        size = 5
                        
                    self.desenhar_cubo(frame, cx, cy, size=size)

        for i in range(4):
            if active_touches[i] and not self.playing[i]:
                self.sounds[i].play(-1)
                self.playing[i] = True
            elif not active_touches[i] and self.playing[i]:
                self.sounds[i].stop()
                self.playing[i] = False
                    
        return frame