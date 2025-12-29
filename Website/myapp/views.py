from django.http import StreamingHttpResponse
from django.conf import settings
from .detector import TrafficDetector
import os
from .models import Document
from django.shortcuts import render


MODEL_PATH = os.path.join(settings.BASE_DIR, 'myapp', 'media', 'model_4', 'model_4.pt')
detector = TrafficDetector(MODEL_PATH)

def handle_file(request):
    if request.method == 'POST' and request.FILES['my_file']:
        # --- UPLOAD METHOD ---
        uploaded_file = request.FILES['my_file']
        doc = Document.objects.create(title="User Upload", uploaded_file=uploaded_file)
        
        # --- READ METHOD (Reading content without saving first) ---
        # Note: Use .read() for small files, .chunks() for large ones
        file_content = uploaded_file.read().decode('utf-8') 
        
        return render(request, 'success.html', {'content': file_content})
    
    
    return render(request, 'upload.html')

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