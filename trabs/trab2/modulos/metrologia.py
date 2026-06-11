import cv2
import numpy as np
import math

class MetrologiaArUco:
    def __init__(self, dict_type=cv2.aruco.DICT_6X6_50, marker_size_cm=5.0):
        self.dictionary = cv2.aruco.getPredefinedDictionary(dict_type)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)
        self.marker_size_cm = marker_size_cm

    def process_frame(self, frame):
        corners, ids, _ = self.detector.detectMarkers(frame)
        
        if ids is not None and len(ids) >= 2:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            c1 = np.mean(corners[0][0], axis=0)
            c2 = np.mean(corners[1][0], axis=0)
            
            pixel_distance = math.dist(c1, c2)
            
            p1_c1 = corners[0][0][0]
            p2_c1 = corners[0][0][1]
            marker_pixel_size = math.dist(p1_c1, p2_c1)
            
            if marker_pixel_size > 0:
                cm_per_pixel = self.marker_size_cm / marker_pixel_size
                real_distance = pixel_distance * cm_per_pixel
                
                cv2.line(frame, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (0, 255, 0), 2)
                cv2.putText(frame, f"{real_distance:.2f} cm", 
                            (int((c1[0]+c2[0])/2), int((c1[1]+c2[1])/2) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame