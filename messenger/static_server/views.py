from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password

from user.models import User

import requests


def proof(request):
    if request.method == "GET":
        return render(request, '11C88FED60032AE0E360C99C0259128C.txt')
    else:
        return HttpResponseNotAllowed()


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

@csrf_protect
def lp_login(request):
    if request.method == "GET":
        return render(request, 'lp-login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            user = get_object_or_404(User.objects.all(), username=username)
            if user.check_password(password):
                request.session['username'] = user.id
                request.user = user
                return render(request, 'home.html')
            else:
                return render(request, 'lp-login.html')
        else:
            return HttpResponse('reCAPTCHA failed')
    else:
        return HttpResponseNotAllowed()


@csrf_protect
@login_required(login_url='/lp-login/')
def home(request):
    if request.method == "GET":
        print('User: ', request.user)
        return render(request, 'home.html')
    else:
        return HttpResponseNotAllowed()
