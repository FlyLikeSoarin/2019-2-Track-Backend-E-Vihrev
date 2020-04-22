from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    else:
        return HttpResponseNotAllowed()

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        return HttpResponseNotAllowed()

@login_required
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')
    else:
        return HttpResponseNotAllowed()
