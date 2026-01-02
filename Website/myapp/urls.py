from django.urls import path, include
import myapp.views as views
import django.contrib.admin as admin

urlpatterns = [
    path('api/', include('api.urls')),
    path('', views.menu, name='menu'),
    path('traffic/', views.traffic_view, name='traffic'),
    path('about/', views.about, name='about'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('detect/<int:file_id>/', views.detect_stream, name='detect_stream'),
]