from django.shortcuts import render, redirect
from django.http import HttpResponse
# from rest_framework.response import Response
# Create your views here.
from .models import *
from .forms import *
from django.http import StreamingHttpResponse


def main(request):
    data = Videos.objects.all()
    return render(request,'streaming.html',{'data':data})

#Arduino를 이용한 영상 받아서 뿌려주고 1분 단위로 영상 전달하게 설정

from django.http import StreamingHttpResponse, HttpResponse
from django.utils.http import http_date
import os
from django.conf import settings
import re

def get_file_chunk(file_path, offset=0, chunk_size=8192):
    with open(file_path, 'rb')as f:
        f.seek(offset)
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

def stream_video(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(file_path):
        return HttpResponse(status=404)
    
    range_header = request.META.get('HTTP_RANGE','').strip()
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)

    file_size = os.path.getsize(file_path)
    start = 0
    end = file_size - 1

    if range_match:
        start = int(range_match.group(1))
        if range_match.group(2):
            end = int(range_match.group(2))

    content_lenght = (end - start)+1
    response = StreamingHttpResponse(get_file_chunk(file_path, offset=start),status=206)
    response['Content-Length'] = str(content_lenght)
    response['Content-Range'] = f'bytes {start} - {end}/{file_size}'
    response['Accept-Ranges'] = 'bytes'
    response['Last-Modified'] = http_date(os.path.getmtime(file_path))
    response['Cache-Control'] = 'no-cache'
    response['Content-Type'] = 'video/mp4'

    return response

import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def upload_video(request):
    return render(request,'upload.html')


@csrf_exempt
def upload(request):
    if request.method == "POST" and request.FILES['video']:
        video_file = request.FILES['video']
        save_path = os.path.join(settings.MEDIA_ROOT, 'video', video_file.name)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb+')as f:
            for chunk in video_file.chunks():
                f.write(chunk)
    
        return JsonResponse({"message":"비디오 업로드 성공",'file_path':save_path})
    
    return JsonResponse({"error":"유요한 결과"},status=400)