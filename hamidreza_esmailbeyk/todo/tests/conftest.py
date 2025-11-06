import pytest
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_todo(test_user):
    return Todo.objects.create(
        todo_title='Test Todo',
        todo_content='Test content',
        todo_priority=15,
        todo_is_done=False,
        user=test_user
    )