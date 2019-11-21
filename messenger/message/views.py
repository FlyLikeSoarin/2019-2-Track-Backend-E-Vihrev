from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

def get_chat_messages():
    if request.method == 'GET':
        # message = {'message-id': id, 'data': messsage-data}
        data = { 'messages': [] }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed()

def send_message():
    if request.method == 'POST':
        # sending logic
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed()
