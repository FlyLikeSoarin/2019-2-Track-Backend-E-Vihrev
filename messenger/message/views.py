from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from rest_framework.viewsets import ModelViewSet

from message.serializers import MessageSerializer
from message.models import Message


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookupfield = 'id'
    lookup_url_kwarg = 'id'


def get_chat_messages():
    if request.method == 'GET':
        # message = {'message-id': id, 'data': messsage-data}
        data = {'messages': []}
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed()

def send_message():
    if request.method == 'POST':
        # if request.POST.get('type') and if request.GET.get('id')::
        #     id = request.GET['type']
        #     type = request.GET['id']
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed()
