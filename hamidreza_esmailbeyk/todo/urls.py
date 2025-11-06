from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TodosAllCURDWithViewSetsAPIView, basename='todo')

urlpatterns = [
    # Function Based Views
    path('', view=views.all_todos, name='all_todos'),
    path('<int:todo_id>/', view=views.todo_detail_view, name='todo_detail_view'),
    
    # Class Based Views
    path('cbv/', view=views.TodosListAPIView.as_view(), name='todos_list_cbv'),
    path('cbv/<int:todo_id>/', view=views.TodoDetailAPIView.as_view(), name='todo_detail_cbv'),
    
    # Mixins
    path('mixins/', view=views.TodosListMixinAPIView.as_view(), name='todos_list_mixin'),  
    path('mixins/<int:pk>/', view=views.TodosDetaileMixinAPIView.as_view(), name='todo_detail_mixin'),  
    
    # Generics
    path('generics/', view=views.TodosListAndCreateGenericsAPIView.as_view(), name='todos_list_generic'),  
    path('generics/<int:pk>/', view=views.TodoRetrieveAndUpdateAndDestroyAPIView.as_view(), name='todo_detail_generic'),  
    
    # ViewSets
    path('viewsets/', include(router.urls), name='todos_viewset'),
    
    # Users
    path('users/', view=views.AllUsersViewSetsAPIView.as_view(), name='all_users'),
]