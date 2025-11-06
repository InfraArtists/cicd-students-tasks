from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from todo.models import Todo

User = get_user_model()

class TodoViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            todo_title='Test Todo',
            todo_content='Test content',
            todo_priority=15,
            todo_is_done=False,
            user=self.user
        )
        self.list_url = reverse('todo-list')
        self.detail_url = reverse('todo-detail', kwargs={'pk': self.todo.pk})

    def test_get_todos_list(self):
        """Test retrieving list of todos"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_todo(self):
        """Test creating a new todo"""
        data = {
            'todo_title': 'New Todo',
            'todo_content': 'New content',
            'todo_priority': 12,
            'todo_is_done': False,
            'user': self.user.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['todo_title'], 'New Todo')

    def test_get_todo_detail(self):
        """Test retrieving todo detail"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['todo_title'], 'Test Todo')

    def test_update_todo(self):
        """Test updating todo"""
        data = {
            'todo_title': 'Updated Todo',
            'todo_content': 'Updated content',
            'todo_priority': 18,
            'todo_is_done': True,
            'user': self.user.id
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['todo_title'], 'Updated Todo')
        self.assertEqual(response.data['todo_is_done'], True)

    def test_delete_todo(self):
        """Test deleting todo"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

class FunctionBasedViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            todo_title='Test Todo',
            todo_content='Test content',
            todo_priority=15,
            todo_is_done=False,
            user=self.user
        )

    def test_all_todos_get(self):
        """Test GET all_todos function view"""
        url = '/todos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_all_todos_post(self):
        """Test POST all_todos function view"""
        url = '/todos/'
        data = {
            'todo_title': 'New Function Todo',
            'todo_content': 'New content',
            'todo_priority': 14,
            'todo_is_done': False,
            'user': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todo_detail_view_get(self):
        """Test GET todo_detail_view"""
        url = f'/todos/{self.todo.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_detail_view_put(self):
        """Test PUT todo_detail_view"""
        url = f'/todos/{self.todo.id}/'
        data = {
            'todo_title': 'Updated Todo',
            'todo_content': 'Updated content',
            'todo_priority': 16,
            'todo_is_done': True,
            'user': self.user.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_todo_detail_view_delete(self):
        """Test DELETE todo_detail_view"""
        url = f'/todos/{self.todo.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ClassBasedViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            todo_title='Test Todo',
            todo_content='Test content',
            todo_priority=15,
            todo_is_done=False,
            user=self.user
        )

    def test_todos_list_api_view_get(self):
        """Test GET TodosListAPIView"""
        url = '/todos/cbv/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todos_list_api_view_post(self):
        """Test POST TodosListAPIView"""
        url = '/todos/cbv/'
        data = {
            'todo_title': 'New CBV Todo',
            'todo_content': 'New content',
            'todo_priority': 13,
            'todo_is_done': False,
            'user': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todo_detail_api_view_get(self):
        """Test GET TodoDetailAPIView"""
        url = f'/todos/cbv/{self.todo.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_not_found(self):
        """Test non-existent todo returns 404"""
        url = '/todos/cbv/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)