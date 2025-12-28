from django.urls import path, include
import myapp.views as views
import django.contrib.admin as admin
from myapp import views

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', views.menu, name='menu'),
    path('traffic/', views.traffic_view, name='traffic'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('about/', views.about, name='about'),
]