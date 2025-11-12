from django.test import TestCase
from django.contrib.auth import get_user_model
from todo.serializers import TodoSerialaizer, UserSerialaizer
from todo.models import Todo

User = get_user_model()

class TodoSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.valid_data = {
            'todo_title': 'Test Todo',
            'todo_content': 'Test content',
            'todo_priority': 15,
            'todo_is_done': False,
            'user': self.user.id
        }

    def test_valid_serializer(self):
        """Test serializer with valid data"""
        serializer = TodoSerialaizer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_priority_too_low(self):
        """Test serializer with priority less than 10"""
        invalid_data = self.valid_data.copy()
        invalid_data['todo_priority'] = 5
        serializer = TodoSerialaizer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('todo_priority', serializer.errors)

    def test_invalid_priority_too_high(self):
        """Test serializer with priority greater than 20"""
        invalid_data = self.valid_data.copy()
        invalid_data['todo_priority'] = 25
        serializer = TodoSerialaizer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('todo_priority', serializer.errors)

    def test_serializer_fields(self):
        """Test serializer contains all expected fields"""
        todo = Todo.objects.create(
            todo_title='Test',
            todo_content='Content',
            todo_priority=15,
            todo_is_done=False,
            user=self.user
        )
        serializer = TodoSerialaizer(todo)
        expected_fields = ['id', 'todo_title', 'todo_content', 'todo_priority', 'todo_is_done', 'user']
        self.assertEqual(list(serializer.data.keys()), expected_fields)

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            todo_title='User Test Todo',
            todo_content='Content',
            todo_priority=15,
            todo_is_done=False,
            user=self.user
        )

    def test_user_serializer_with_todos(self):
        """Test user serializer includes todos"""
        serializer = UserSerialaizer(self.user)
        self.assertIn('todos', serializer.data)
        self.assertEqual(len(serializer.data['todos']), 1)
        self.assertEqual(serializer.data['todos'][0]['todo_title'], 'User Test Todo')