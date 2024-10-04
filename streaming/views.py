from django.shortcuts import render, redirect
from django.http import HttpResponse
# from rest_framework.response import Response
# Create your views here.
from .models import *
from .forms import *
def main(request):
    data = Videos.objects.all()
    return render(request,'streaming.html',{'data':data})

import cv2


def record_video(video_path, duration=60):
    print(f'video path:{video_path}')
    cap = cv2.VideoCapture(video_path)  
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    # 프레임 속도가 유효한지 확인
    if frame_rate is None or frame_rate <= 0:
        print("Error: frame_rate_error")
        return  # 유효한 프레임 속도가 없으면 함수 종료

    try:
        frame_rate = float(frame_rate)
    except ValueError:
        print("Error: frame rate is not a valid number")
        return

    # 분당 프레임 수 계산
    frame_per_minute = int(frame_rate * duration)

    out = None
    current_frame = 0
    segment_number = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
    
        if not ret:
            break
            
        # 새로운 비디오 세그먼트를 만들 시간인지 확인
        if current_frame % frame_per_minute == 0:
            if out is not None:
                out.release()  # 이전 비디오 파일 닫기

            video_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_segment_{segment_number}.mp4"
            out_file_path = os.path.join(video_path, video_name)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(out_file_path, fourcc, frame_rate, (frame.shape[1], frame.shape[0]))
            segment_number += 1
            
            # 비디오 인스턴스 저장
            try:
                video_instance = Videos(path=out_file_path, file=video_name)  # video_path가 아니라 out_file_path를 사용해야 합니다.
                video_instance.save()    
            except Exception as e:
                print(f"Error saving video: {e}")

        out.write(frame)  # 현재 프레임을 비디오 파일에 작성
        current_frame += 1

    cap.release()  # 비디오 캡처 해제
    if out is not None:
        out.release() 

import datetime
import os

def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        print(video_file)
        if not video_file:
            return render(request,'upload.html',{'form': VideoUploadForm(), "error":'비디오 파일이 없습니다.'})


        video_name = video_file.name #[:-4]
        video_path = os.path.join('media/video', video_name)

        os.makedirs(os.path.dirname(video_path), exist_ok=True)

        
        with open(video_path,'wb+')as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        record_video(video_name, video_path)
        
        return redirect('streaming:main')
    else:
        print(form.errors)
        form = VideoUploadForm()
    
    return render(request,'upload.html', {'form':form})

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