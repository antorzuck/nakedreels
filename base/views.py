from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def video(request):
    return render(request, 'video.html')