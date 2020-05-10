from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.decorators.cache import cache_page

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from chat.serializers import ChatSerializer, MemberSerializer
from message.serializers import MessageSerializer
from message.models import Message
from chat.models import Chat
from user.models import User


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookupfield = 'id'
    lookup_url_kwarg = 'id'

    @cache_page(60)
    @action(detail=True, methods=['get'])
    def list_messages(self, request, id=None):
        chat = get_object_or_404(self.queryset, id=id)
        serializer = MessageSerializer(
            Message.objects.filter(chat=chat),
            many=True)
        return Response(
            {'messages': serializer.data},
            status=status.HTTP_200_OK)

    @cache_page(60)
    @action(detail=True, methods=['post'])
    def send_message(self, request, id=None):
        chat = get_object_or_404(self.queryset, id=id)
        user = get_object_or_404(User.objects.all(), username=request.user)
        try:
            message = Message(
                user=request.user,
                chat=chat,
                text=request.data['text'],
            )
            message.save()

            serializer = MessageSerializer(message)
            return Response({'message': serializer.data}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


def get_chat_data(request):
    if request.method == 'GET':
        data = { 'chat-id': 'undefined', 'users-id': [], 'icon': 'null' }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed()


@cache_page(60)
def list_chats(request):
    if request.method == 'GET':
        chat_data = Chat.objects.all()
        formated_chats = [{
                'chat_id': entry.id,
                'displayName': entry.chat_label,
                'icon': 'undefined' if entry.icon is None else entry.icon,
                'lastMessage': {'text': 'No messages...', 'timestamp': '00:00', 'status': 'undefined'},
                # 'lastMessage': Message.get_last_message,
            }
            for entry in chat_data
        ]

        # dialog_data = Dialog.get_dialogs(my_id)
        # formated_dialogs = [{
        #         'type': 'dialog',
        #         'chat_id': entry.id,
        #         'user_id': entry.second_user.id if my_id != entry.first_user else entry.first_user.id,
        #         'displayName': entry.second_user.username if my_id != entry.first_user else entry.first_user.username,
        #         'icon': 'undefined',
        #         'lastMessage': {'text': 'No messages...', 'timestamp': '00:00', 'status': 'undefined'},
        #     }
        #     for entry in dialog_data
        # ]
        return JsonResponse(formated_chats, safe=False)
    else:
        return HttpResponseNotAllowed()

# def start_dialog(request):
#     if request.method == 'GET':
#         if request.GET.get('id'):
#             id = request.GET['id']
#             Dialog.create_dialog(my_id, id)
#             return HttpResponse(status=200)
#     return HttpResponse(status=204)
