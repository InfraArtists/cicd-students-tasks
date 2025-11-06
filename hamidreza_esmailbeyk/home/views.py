from django.shortcuts import render
from todo.models import Todo
from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.


def index_page(request : HttpRequest):
    context = {
        'todos' : Todo.objects.order_by('todo_priority').all()
    }
    return render(request, 'home/index.html', context=context)

@api_view(["GET"])
def todos_json(request : Request):
    todos = list(Todo.objects.order_by('todo_priority').all().values("todo_title","todo_is_done"))
    return Response(
        {
            "todos" : todos,
            "extra" : "python"
        },
        status=status.HTTP_200_OK,
    )