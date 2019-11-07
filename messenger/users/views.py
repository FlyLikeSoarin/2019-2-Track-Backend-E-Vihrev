from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

def get_my_profile(request):
    if request.method == 'GET':
        data = { 'displayed-name': 'undefined', 'icon': 'null', 'is-friend': 'false', 'user-id': 'undefined' }
        return JsonResponse(data)
    else:
        return HttpResponseForbidden()

def get_user_profile(request):
    if request.method == 'GET':
        data = { 'displayed-name': 'undefined', 'icon': 'null', 'is-friend': 'false' }
        return JsonResponse(data)
    else:
        return HttpResponseForbidden()

def get_user_friends(request):
    if request.method == 'GET':
        data = { 'users-id': [] }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseForbidden()

def get_user_chats(request):
    if request.method == 'GET':
        data = { 'chats-id': [] }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseForbidden()

def register_user(request):
    if request.method == 'POST':
        # registration logic
        return HttpResponse(status=200)
    else:
        return HttpResponseForbidden()
