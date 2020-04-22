from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from user.serializers import UserSerializer
from user.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookupfield = 'id'
    lookup_url_kwarg = 'id'

    # def list(self, request):
    #     pass

    # def get(self, request):
    #     if request.method == 'GET':
    #         id, username = request.GET.get('id'), request.GET.get('username')
    #         user = None
    #         user = User.get_by_id(id) if id else user
    #         user = User.get_by_username(username) if username else user
    #         if user is None:
    #             return Response({}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             serializer = UserSerializer(user)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response({}, status=status.HTTP_403_FORBIDDEN)
    #
    # def current(self, request):
    #     pass


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
