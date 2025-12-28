from django.http import StreamingHttpResponse
from django.conf import settings
from django.http import JsonResponse
from .detector import TrafficDetector
from .models import UploadFile
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import os
import base64


MODEL_PATH = os.path.join(settings.BASE_DIR, 'myapp', 'media', 'model_4', 'model_4.pt')
detector = TrafficDetector(MODEL_PATH)

def video_feed(request):
    detector = TrafficDetector('model_4/model_4.pt')
    video_path = 'myapp/media/traffic_video2.mp4'  # Update this path
    return StreamingHttpResponse(
        detector.get_frames(video_path),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

@require_http_methods(["GET", "POST"])
def upload_and_detect(request):
    if not request.FILES.get('file'):
        return JsonResponse({'error' : 'no file provided'}, status=400)
    
    uploaded_file = request.FILES['file']

    allowed_types = ['video/mp4','image/jpeg','image/png']
    if uploaded_file.content_type not in allowed_types:
        return JsonResponse({'error': 'invalid file type'}, status=400)
        
    if uploaded_file.size > 50 * 1024 * 1024:
        return JsonResponse({'error': 'file too large'}, status=400)
    
    temp_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    try:
        detector = TrafficDetector('model_4/model_4.pt')

        if uploaded_file.content_type == 'video/mp4':
            return StreamingHttpResponse(
                detector.get_frames(temp_path),
                content_type='multipart/x-mixed-replace; boundary=frame'
            )
        else:
            import cv2
            frame = cv2.imread(temp_path)
            results = detector.model.predict(frame, conf=0.5, verbose=False)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

            for box in boxes:
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
            
            cv2.putText(frame, f"Detected: {len(boxes)} objects", (20, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            
            _, buffer = cv2.imencode('.jpg', frame)
            b64_data = base64.b64encode(buffer).decode('utf-8')
            return JsonResponse({
                'success': True,
                'objects_detected': len(boxes),
                'image': 'data:image/jpeg;base64,{b64_data}'
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
def traffic_view(request):
    return render(request, 'traffic_system.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        if uploaded_file.size > 50 * 1024 * 1024:
            return JsonResponse({'error': 'file too large'}, status=400)
        
        allowed_types = ['video/mp4','image/jpeg','image/png']
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({'error': 'invalid file type'}, status=400)
        
        file_obj = UploadFile.objects.create(
            file=uploaded_file,
            file_name=uploaded_file.name
        )

        return JsonResponse({'success': True, 'file_id': file_obj.id})
    return JsonResponse({'error': 'Invalid request'},status=400)