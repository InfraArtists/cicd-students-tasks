from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class TodoAPIIntegrationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.todo_data = {
            'todo_title': 'Integration Test Todo',
            'todo_content': 'Integration test content',
            'todo_priority': 15,
            'todo_is_done': False,
            'user': self.user.id
        }

    def test_full_todo_lifecycle(self):
        """Test complete CRUD lifecycle for Todo"""
        # Create
        create_url = reverse('todo-list')
        response = self.client.post(create_url, self.todo_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        todo_id = response.data['id']

        # Read
        detail_url = reverse('todo-detail', kwargs={'pk': todo_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['todo_title'], 'Integration Test Todo')

        # Update
        update_data = self.todo_data.copy()
        update_data['todo_title'] = 'Updated Integration Todo'
        update_data['todo_is_done'] = True
        response = self.client.put(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['todo_title'], 'Updated Integration Todo')

        # Delete
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_priority_validation(self):
        """Test priority validation across all endpoints"""
        invalid_data = self.todo_data.copy()
        invalid_data['todo_priority'] = 5  # Too low
        
        # Test with function view
        url = '/todos/'
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with class-based view
        url = '/todos/cbv/'
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)