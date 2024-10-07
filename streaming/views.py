from django.shortcuts import render, redirect
from django.http import HttpResponse
# from rest_framework.response import Response
# Create your views here.
from .models import *
from .forms import *


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
# 카메라를 통해 영상 스트리밍 되는지 확인하기위해
def upload_video(request):
    return render(request, 'upload.html')


# 파일 경로 지정 하는 코드
# def upload_video(request):
#     if request.method == "POST":
#         video = request.FILES.get('video')

#         if video:
#             file_path = os.path.join(settings.MEDIA_ROOT, video.name)

#             with open(file_path, 'wb+')as f:
#                 for chunk in video.chunks():
#                     f.write(chunk)
            
#             return render(request, 'main.html', {'filename':video.name})
#     return render(request, 'main.html')


#ESP32-CAM을 이용한 스트리밍 1분마다 저장 **ESP연결부터 진행 필요
# def record_stream():
#     stream_url = "http://<ESP32_IP>/stream"  # ESP32-CAM의 스트리밍 URL로 교체
#     cap = cv2.VideoCapture(stream_url)

#     if not cap.isOpened():
#         print("Error: Unable to open video stream.")
#         return

#     # 비디오 저장을 위한 설정
#     frame_rate = 30  # 프레임 속도 설정
#     frame_count = 0  # 프레임 카운터
#     segment_duration = 60 * frame_rate  # 1분 동안의 프레임 수

#     out = None  # 비디오 작성을 위한 VideoWriter 객체
#     segment_number = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # 프레임 저장
#         if frame_count % segment_duration == 0:
#             # 이전 비디오 파일 닫기
#             if out is not None:
#                 out.release()

#             # 새로운 비디오 파일명 생성
#             video_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_segment_{segment_number}.mp4"
#             out_file_path = os.path.join('media/video', video_name)

#             # VideoWriter 객체 생성
#             fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#             out = cv2.VideoWriter(out_file_path, fourcc, frame_rate, (frame.shape[1], frame.shape[0]))
#             segment_number += 1
            
#             # 비디오 인스턴스 저장
#             try:
#                 video_instance = Videos(path=out_file_path, file=video_name)
#                 video_instance.save()    
#             except Exception as e:
#                 print(f"Error saving video: {e}")

#         # 프레임 쓰기
#         if out is not None:
#             out.write(frame)

#         frame_count += 1

#     cap.release()  # 비디오 캡처 해제
#     if out is not None:
#         out.release()