from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from . import models

my_id = 1; # Temporary. We don't have session system yet.

def get_my_profile(request):
    if request.method == 'GET':
        data = { 'displayed-name': 'undefined', 'icon': 'null', 'is-friend': 'false', 'user-id': 'undefined' }
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed()

def get_user_profile(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            id = request.GET['id']
            entry = models.User.get_by_id(id)
            formated_data = {
                'id': entry.id,
                'username': entry.username,
                'avatar': 'null' if entry.avatar is None else entry.avatar,
            }
            return JsonResponse(formated_data)

        if request.GET.get('search'):
            search_term = request.GET['search']
            data = models.User.search_for_user(search_term)
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

        return HttpResponseNotAllowed()
    else:
        return HttpResponseNotAllowed()

def get_user_friends(request):
    if request.method == 'GET':
        data = { 'users-id': [] }
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed()

def register_user(request):
    if request.method == 'POST':
        # registration logic
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed()
