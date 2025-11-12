from django.test import TestCase
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class TodoModelTest(TestCase):
    def setUp(self):
        """Setup test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            todo_title='Test Todo',
            todo_content='Test content for todo',
            todo_priority=15,
            todo_is_done=False,
            user=self.user
        )

    def test_todo_creation(self):
        """Test todo object creation"""
        self.assertEqual(self.todo.todo_title, 'Test Todo')
        self.assertEqual(self.todo.todo_content, 'Test content for todo')
        self.assertEqual(self.todo.todo_priority, 15)
        self.assertEqual(self.todo.todo_is_done, False)
        self.assertEqual(self.todo.user.username, 'testuser')

    def test_todo_string_representation(self):
        """Test string representation of todo"""
        expected_string = f"{self.todo.todo_title}/ Is done : {self.todo.todo_is_done}"
        self.assertEqual(str(self.todo), expected_string)

    def test_todo_table_name(self):
        """Test custom table name"""
        self.assertEqual(self.todo._meta.db_table, 'todos')

    def test_todo_user_relationship(self):
        """Test relationship between todo and user"""
        self.assertEqual(self.todo.user, self.user)
        self.assertIn(self.todo, self.user.todos.all())