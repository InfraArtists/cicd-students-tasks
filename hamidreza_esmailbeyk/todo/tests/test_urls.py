from django.test import TestCase
from django.urls import reverse, resolve
from todo import views

class UrlTests(TestCase):
    def test_all_todos_url(self):
        """Test all_todos URL"""
        url = reverse('all_todos')
        self.assertEqual(resolve(url).func, views.all_todos)

    def test_todo_detail_url(self):
        """Test todo_detail_view URL"""
        url = reverse('todo_detail_view', args=[1])
        self.assertEqual(resolve(url).func, views.todo_detail_view)

    def test_todos_list_cbv_url(self):
        """Test TodosListAPIView URL"""
        url = reverse('todos_list_cbv')
        self.assertEqual(resolve(url).func.view_class, views.TodosListAPIView)

    def test_todo_detail_cbv_url(self):
        """Test TodoDetailAPIView URL"""
        url = reverse('todo_detail_cbv', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TodoDetailAPIView)

    def test_todos_list_mixin_url(self):
        """Test TodosListMixinAPIView URL"""
        url = reverse('todos_list_mixin')
        self.assertEqual(resolve(url).func.view_class, views.TodosListMixinAPIView)

    def test_todo_detail_mixin_url(self):
        """Test TodosDetaileMixinAPIView URL"""
        url = reverse('todo_detail_mixin', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TodosDetaileMixinAPIView)

    def test_todos_list_generic_url(self):
        """Test TodosListAndCreateGenericsAPIView URL"""
        url = reverse('todos_list_generic')
        self.assertEqual(resolve(url).func.view_class, views.TodosListAndCreateGenericsAPIView)

    def test_todo_detail_generic_url(self):
        """Test TodoRetrieveAndUpdateAndDestroyAPIView URL"""
        url = reverse('todo_detail_generic', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TodoRetrieveAndUpdateAndDestroyAPIView)

    def test_all_users_url(self):
        """Test AllUsersViewSetsAPIView URL"""
        url = reverse('all_users')
        self.assertEqual(resolve(url).func.view_class, views.AllUsersViewSetsAPIView)