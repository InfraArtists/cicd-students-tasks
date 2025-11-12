from rest_framework import serializers
from .models import Todo, user


class TodoSerialaizer(serializers.ModelSerializer):
    
    # def validate(self, attrs):
    #     print(attrs)
    #     return super().validate(attrs)
    
    def validate_todo_priority(self, todo_priority):
        if todo_priority < 10 or todo_priority > 20:
            raise serializers.ValidationError("todo_priority must be between 1 - 10 ")
        return todo_priority
    
    
    class Meta:
        model = Todo
        # fields = ["id", "todo_title", "todo_content", "todo_priority", "todo_is_done"] # same below
        fields = "__all__"
        
        
class UserSerialaizer(serializers.ModelSerializer):
    todos = TodoSerialaizer(read_only = True, many = True)
    
    class Meta:
        model = user
        # fields = ["id", "todo_title", "todo_content", "todo_priority", "todo_is_done"] # same below
        fields = "__all__"

        