from django.shortcuts import render, redirect
from django.http import HttpResponse
# from rest_framework.response import Response
# Create your views here.
from .forms import *
def main(request):
    return render(request,'streaming.html')

import cv2
import time

def record_video(video_path,video_name, duration=60):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_forcc(*'mp4v')
    out = cv2.VideoWriter(video_name, fourcc, 20.0, (640,480))

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
    
        if not ret:
            break
    
        if time.time() - start_time >= duration:
            out.write(frame)
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_path = request.FILES.get('video').temporary_file_path()
            video_name = form.cleaned_data.get('video').name

            record_video(video_path, video_name)
            # return Response({'message':'비디오 저장 완료'}, status=200)
        else:
            form = VideoUploadForm()
        
        return render(request,'upload.html', {'form':form})

