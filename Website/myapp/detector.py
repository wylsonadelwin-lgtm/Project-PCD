import cv2
import os
import time
import numpy as np
from ultralytics import YOLO
from django.conf import settings

class TrafficDetector:
    def __init__(self, model_rel_path):
        self.model_path = os.path.join(settings.MEDIA_ROOT, model_rel_path)
        self.model = YOLO(self.model_path)

    def process_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()

        if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            return self.process_image(file_path)
        elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
            return self.get_frames(file_path)
        else:
            return None

    def process_image(self, image_path):
        frame = cv2.imread(image_path)
        if frame is None:
            return
            
        results = self.model.predict(frame, conf=0.5, verbose=False)
        annotated_frame = results[0].plot()
        
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def get_frames(self, video_path):
        current_timer = 10
        last_time_update = time.time()
        lampu_state = "RED"
        total_objek = 0


        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            results = self.model.predict(frame, conf=0.5, verbose=False)
            annotated_frame = results[0].plot() 

            if time.time() - last_time_update >= 1:
                if current_timer > 0:
                    current_timer -= 1
            last_time_update = time.time()

            if current_timer <= 0:
                if lampu_state == "RED":
                    lampu_state = "GREEN"
                    current_timer = 20 if total_objek > 20 else 10

            else:
                lampu_state = "RED"
                current_timer = 30 if total_objek > 20 else 15

            color_map = {
                "RED" : (0, 0, 255),
                "GREEN" : (0, 255, 0)
            }
            current_color = color_map[lampu_state]

            cv2.putText(frame, f"lampu: {lampu_state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 2)

            _, buffer = cv2.imencode('.jpg', annotated_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cap.release()

