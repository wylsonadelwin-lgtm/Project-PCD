from django.shortcuts import render
from .models import Task 
from .serializers import TaskSerializer
from rest_framework import generics

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Create your views here.
