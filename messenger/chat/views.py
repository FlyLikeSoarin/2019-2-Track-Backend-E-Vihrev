from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed

def get_chat_data(request):
    if request.method == 'GET':
        data = { 'chat-id': 'undefined', 'users-id': [], 'icon': 'null' }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed()
