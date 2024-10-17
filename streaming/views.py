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



import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def upload_video(request):
    return render(request,'upload.html')

import ffmpeg
import datetime
import subprocess
@csrf_exempt
def upload(request):
    if request.method == "POST" and request.FILES['video']:
        if 'video' in request.FILES:
            video_file = request.FILES['video']
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
            save_path = os.path.join(settings.MEDIA_ROOT, 'video', f"{timestamp}.webm")

            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            try:
                    # 웹에서 업로드된 비디오 저장
                    with open(save_path, 'wb+') as f:
                        for chunk in video_file.chunks():
                            f.write(chunk)

                    # 변환할 경로 설정
                    output_path = save_path.replace('.webm', '.mp4')
                    command = ['ffmpeg', '-i', save_path, output_path]
                    result = subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

                    return JsonResponse({"message": "비디오 업로드 및 변환 성공", 'file_path': output_path})

            except Exception as e:
                # 오류 발생 시 로그 출력
                print(f"Error during video processing: {str(e)}")
                return JsonResponse({"error": "비디오 처리 중 오류가 발생했습니다."}, status=500)

        return JsonResponse({"error": "비디오 파일이 필요합니다."}, status=400)

    return JsonResponse({"error": "POST로 전달 해야합니다."}, status=400)

