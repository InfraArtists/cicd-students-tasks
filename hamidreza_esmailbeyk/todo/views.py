from django.shortcuts import render
from django.http import Http404
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerialaizer, UserSerialaizer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import user

# Create your views here.



# function base view methodes

# CRUD

# CR from CRUD
@extend_schema(
        request=TodoSerialaizer,
        responses={201: TodoSerialaizer},
        description="this api use for class base view api"
    )

@api_view(['GET', 'POST'])
def all_todos(request : Request):

    if request.method == "GET":
        todos = Todo.objects.order_by("todo_priority").all()
        todo_serializer = TodoSerialaizer(todos, many = True)
        return Response(
            todo_serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == "POST":
        todo_deserializer = TodoSerialaizer(data = request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(
                todo_deserializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                todo_deserializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(None,status=status.HTTP_400_BAD_REQUEST)
    
    
    
# RUD from CRUD
@extend_schema(
        request=TodoSerialaizer,
        responses={201: TodoSerialaizer},
        description="this api use for class base view api"
    )
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request : Request, todo_id : int):
    try:
        todo = Todo.objects.get(pk = todo_id)
    except Todo.DoesNotExist:
        return Response(
            None,
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        todo_serializer = TodoSerialaizer(todo, many = False)
        return Response(
            todo_serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == "PUT":
        todo_deserializer = TodoSerialaizer(todo, data = request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(
                data=todo_deserializer.data,
                status=status.HTTP_202_ACCEPTED,
                )
        else:
            return Response(
                None,
                status=status.HTTP_404_NOT_FOUND,
            )
   
    elif request.method == "DELETE":
        todo.delete()
        return Response(
            data=None,
            status=status.HTTP_204_NO_CONTENT,
        )
        
    else:
        return Response(None,status=status.HTTP_400_BAD_REQUEST)
    
    


# class base view methodes

@extend_schema(
        request=TodoSerialaizer,
        responses={201: TodoSerialaizer},
        description="this api use for class base view api"
    )
class TodosListAPIView(APIView):
    def get(self, request : Request):
        todos = Todo.objects.order_by("todo_priority").all()
        todos_serializer = TodoSerialaizer(todos, many = True)
        return Response(
            data=todos_serializer.data,
            status=status.HTTP_200_OK,
        )
    
    def post(self, request : Request):
        todo_deserializer = TodoSerialaizer(data = request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(
                todo_deserializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                todo_deserializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
@extend_schema(
        request=TodoSerialaizer,
        responses={201: TodoSerialaizer},
        description="this api use for class base view api"
    )          
class TodoDetailAPIView(APIView):
    def get_object(self, todo_id : int):
        try:
            todo = Todo.objects.get(pk = todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(
                None,
                status=status.HTTP_404_NOT_FOUND,
            )
    def get(self, request : Request, todo_id : int):
        todo = self.get_object(todo_id=todo_id)
        if isinstance(todo, Response):
            return todo
        todo_serializer = TodoSerialaizer(todo, many = False)
        return Response(
            todo_serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request : Request, todo_id : int):
        todo = self.get_object(todo_id=todo_id)
        if isinstance(todo, Response):
            return todo
        todo_deserializer = TodoSerialaizer(todo, data = request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(
                data=todo_deserializer.data,
                status=status.HTTP_202_ACCEPTED,
                )
        else:
            return Response(
                None,
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request : Request, todo_id : int):
        todo : Todo
        todo = self.get_object(todo_id=todo_id)
        if isinstance(todo, Response):
            return todo
        todo.delete()
        return Response(
            data=None,
            status=status.HTTP_204_NO_CONTENT,
        )
        
        


# mixins and generics


class TodosListMixinAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by("todo_priority").all()
    serializer_class = TodoSerialaizer
    
    def get(self, request : Request):
        return self.list(request=request)
    
    def post(self, request : Request):
        return self.create(request=request)



class TodosDetaileMixinAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by("todo_priority").all()
    serializer_class = TodoSerialaizer
    
    def get(self, request : Request, pk : int):
        return self.retrieve(
            request,
            pk,
        )
    
    def put(self, request : Request, pk : int):
        return self.update(
            request,
            pk,
        )

    def delete(self, request : Request, pk : int):
        return self.destroy(
            request,
            pk,
        )



# generics


class TodosGenericPagination(PageNumberPagination):
    page_size = 1


class TodosListAndCreateGenericsAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by("todo_priority").all()
    serializer_class = TodoSerialaizer
    pagination_class = TodosGenericPagination
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 3
    
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    
    
    

class TodoRetrieveAndUpdateAndDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by("todo_priority").all()
    serializer_class = TodoSerialaizer
    pagination_class = TodosGenericPagination
    
    
    
# viewsets


class TodosAllCURDWithViewSetsAPIView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by("todo_priority").all()
    serializer_class = TodoSerialaizer
    pagination_class = LimitOffsetPagination
    
    
    
# users
class AllUsersViewSetsAPIView(generics.ListAPIView):
    queryset = user.objects.all()
    serializer_class = UserSerialaizer
