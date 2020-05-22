from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from user.serializers import UserSerializer
from user.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookupfield = 'id'
    lookup_url_kwarg = 'id'

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            if not self.queryset.filter(username=username, password=password).exists():
                user = UserSerializer.create(validated_data={'username': username, 'password': password})
                serializer = UserSerializer(user)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        serializer = UserSerializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super(UserViewSet, self).get_permissions()


@login_required
def get_my_profile(request):
    if request.method == 'GET':
        user = request.user
        data = { 'displayedName': 'undefined', 'icon': 'null', 'is-friend': 'false', 'user-id': 'undefined' }
        return JsonResponse(data)
    return HttpResponseNotAllowed(['GET'])


def get_user_profile(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            id = request.GET.get('id')
            entry = User.get_by_id(id)
            formated_data = {
                'id': entry.id,
                'displayedName': entry.username,
                'userIcon': 'null' if entry.avatar is None else entry.avatar,
            }
            return JsonResponse(formated_data)

        if request.GET.get('search'):
            search_term = request.GET.get('search')
            data = User.search_for_user(search_term)
            if data is not None:
                formated_data = [{
                        'id': entry.id,
                        'username': entry.username,
                        'avatar': 'null' if entry.avatar is None else entry.avatar,
                    }
                    for entry in data
                ]
                return JsonResponse(formated_data, safe=False)
            else:
                return HttpResponse(status=204)

        return HttpResponse('Bad request', status=400)
    return HttpResponseNotAllowed(['GET'])


def get_user_friends(request):
    if request.method == 'GET':
        data = { 'users-id': [] }
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed(['GET'])


def login(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.get_by_username(username)
            if user.password == password:
                request.session[str(user.id)] = user.id
                return HttpResponse('Logged in', status=200)
            else:
                return HttpResponse('Username/password pair does not exists', status=400)
        return HttpResponse('Bad request', status=400)
    return HttpResponseNotAllowed(['GET'])


# def logout(request):
#     try:
#         del request.session['member_id']
#     except KeyError:
#         pass
#     return HttpResponse("Logged out", status=200)


def register(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not User.get_by_username(username):
                user = User(username=username, password=password)
                User.save(user)
                request.session[str(user.id)] = user.id
                return HttpResponse('Registered', status=200)
            else:
                return HttpResponse('Already_exist', status=400)
        return HttpResponse('Bad request', status=400)
    return HttpResponseNotAllowed(['GET'])
