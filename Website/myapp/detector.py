import cv2
from ultralytics import YOLO
from django.conf import settings
import time
import os

MODEL_PATH = os.path.join(settings.MEDIA_ROOT, 'model_4', 'model_4.pt')
model = YOLO(MODEL_PATH)

class TrafficDetector:
    def __init__(self, model_rel_path):
        self.model_path = os.path.join(settings.MEDIA_ROOT, model_rel_path)
        self.model = YOLO(self.model_path)
        self.lampu_state = "GREEN"
        self.current_timer = 10
        self.last_time_update = time.time()

    def get_frames(self, video_path):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"CRITICAL ERROR: Could not open video file at {video_path}")
            return # Stop here if it failed
        
        frame_count = 0
        skip_frames = 2  
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            frame = cv2.resize(frame, (640, 480))
            frame_count += 1

            if frame_count % skip_frames != 0:
                continue

            # 1. AI Detection
            results = self.model.predict(frame, conf=0.5, verbose=False)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            objects_count = len(boxes)

            # Draw boxes
            for box in boxes:
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)

            # 2. Timer & Logic (Your exact logic from the notebook)
            if time.time() - self.last_time_update >= 1:
                if self.current_timer > 0: self.current_timer -= 1
                self.last_time_update = time.time()

            if self.current_timer <= 0:
                if self.lampu_state == "RED":
                    self.lampu_state = "GREEN"
                    self.current_timer = 20 if objects_count > 20 else 10
                else:
                    self.lampu_state = "RED"
                    self.current_timer = 30 if objects_count > 20 else 15

            # 3. Annotate Frame
            color = (0, 255, 0) if self.lampu_state == "GREEN" else (0, 0, 255)
            cv2.putText(frame, f"STATUS: {self.lampu_state}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            
            # 4. Stream to Web
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        cap.release()