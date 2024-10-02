from django import forms

class VideoUploadForm(forms.ModelForm):
    video = forms.FileField()
    