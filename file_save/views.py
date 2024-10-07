#streaming에서 전달 해주는 1분단위 파일을 저장 경로 데이터베이스 전달


from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse,HttpResponse
import os
import re



# Create your views here.
