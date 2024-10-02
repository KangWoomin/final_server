from django import forms
from .models import User
class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['userID','email','name']

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 다릅니다.')
        
        return self.cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        
        if commit:
            user.save()
            
        return user