from django.urls import path
from . import views

urlpatterns = [
    # path('',view=views.index_page),
    path('',view=views.todos_json),
]
