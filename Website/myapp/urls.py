from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import myapp.views as views
import django.contrib.admin as admin
from myapp import views

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', views.menu, name='menu'),
    path('upload_and_detect/', views.upload_and_detect, name='upload_and_detect'),
    path('upload/', views.upload_file, name='upload'),
    path('traffic/', views.traffic_view, name='traffic'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)