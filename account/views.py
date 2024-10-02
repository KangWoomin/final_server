from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def main(request):
    return render(request, 'base.html')

def create_user(request):
    if request.method == 'POST':
        user = UserCreateForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('main')
    
    else:
        user = UserCreateForm()
    
    return render(request, 'create_user.html', {'user':user})



def user_login(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        password = request.POST.get('password')

        user = authenticate(request, userID = userID, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            content = {
                'error':'로그인에 실패 하셨습니다.'
            }
            return render(request,'user_login.html', content)
    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('main')


