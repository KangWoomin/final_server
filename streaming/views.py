from django.shortcuts import render, redirect
from django.http import HttpResponse
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

    while int(time.time()) - start_time<duration:
        ret, frame = cv2.read()

        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FIELS)
        if form.is_valid():
            video_path = request.FIELS['video']

        else:
            form = VideoUploadForm()
        
        return render(request,'upload.html', {'form':form})

