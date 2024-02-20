from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    #this is test view
    return render(request, 'app/index.html')