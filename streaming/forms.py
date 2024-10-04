from django import forms
from .models import *

class VideoUploadForm(forms.ModelForm):

    class Meta:
        model = Videos
        fields = ['path','file']
        labels = {
            'path' : "비디오 경로" ,
            'file' : '비디오 파일'
        }