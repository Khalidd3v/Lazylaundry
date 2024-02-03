from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login-user/')
def home(request):
    return render(request, 'app/index.html')