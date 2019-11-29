from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from . import models

my_id = 1; # Temporary. We don't have session system yet.

def get_chat_data(request):
    if request.method == 'GET':
        data = { 'chat-id': 'undefined', 'users-id': [], 'icon': 'null' }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed()

def list_chats(request):
    if request.method == 'GET':
        chat_data = models.Chat.get_chats(my_id)
        formated_chats = [{
                'type': 'chat',
                'id': entry.id,
                'chat_label': entry.chat_label,
                'icon': 'null' if entry.icon is None else entry.icon,
            }
            for entry in chat_data
        ]

        dialog_data = models.Dialog.get_dialogs(my_id)
        formated_dialogs = [{
                'type': 'dialog',
                'id': entry.id,
                'receiver': entry.second_user.id if my_id != entry.first_user else entry.first_user.id,
            }
            for entry in dialog_data
        ]
        return JsonResponse(formated_chats + formated_dialogs, safe=False)
    else:
        return HttpResponseNotAllowed()

def start_dialog(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            id = request.GET['id']
            models.Dialog.create_dialog(my_id, id)
            return HttpResponse(status=200)
    return HttpResponse(status=204)
