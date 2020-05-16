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
from chat.models import Chat, Member
from user.models import User


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookupfield = 'id'
    lookup_url_kwarg = 'id'

    @action(detail=False, methods=['get'])
    def list_chats(self, request):
        chats = Member.objects.all().filter(user=request.user).values('chat').distinct()
        chats_id = [entry['chat'] for entry in chats]

        serializer = ChatSerializer(
            self.queryset.filter(id__in=chats_id),
            many=True)

        data = {entry['id']: entry for entry in serializer.data}

        return Response(
            {'chats': data},
            status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_chat(self, request):
        user=request.user
        try:
            chat = Chat(
                creator=request.user,
                chat_label=request.data['chat_label'],)
            chat.save()

            member = Member(
                chat=chat,
                user=request.user,
            )
            member.save()

            serializer = ChatSerializer(chat)
            return Response({'chats': {serializer.data['id']: serializer.data}}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def join_chat(self, request, id=None):
        chat = get_object_or_404(self.queryset, id=id)

        if not Member.objects.all().filter(chat=chat, user=request.user).exists():
            member = Member(
                chat=chat,
                user=request.user,
            )
            member.save()
        
        serializer = ChatSerializer(chat)
        return Response({'chats': {serializer.data['id']: serializer.data}}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def list_messages(self, request, id=None):
        chat = get_object_or_404(self.queryset, id=id)
        serializer = MessageSerializer(
            Message.objects.filter(chat=chat),
            many=True)
        return Response(
            {'chatMessages': {chat.id: serializer.data}},
            status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def send_message(self, request, id=None):
        chat = get_object_or_404(self.queryset, id=id)
        user = get_object_or_404(Member.objects.all().filter(chat=chat), user=request.user)
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
