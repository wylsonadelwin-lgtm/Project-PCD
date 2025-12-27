from django.http import StreamingHttpResponse
from django.conf import settings
from .detector import TrafficDetector
import os
from django.shortcuts import render


MODEL_PATH = os.path.join(settings.BASE_DIR, 'myapp', 'media', 'model_4', 'model_4.pt')
detector = TrafficDetector(MODEL_PATH)

def video_feed(request):
    detector = TrafficDetector('model_4/model_4.pt')
    video_path = 'myapp/media/traffic_video2.mp4'  # Update this path
    return StreamingHttpResponse(
        detector.get_frames(video_path),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def traffic_view(request):
    return render(request, 'traffic_system.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')