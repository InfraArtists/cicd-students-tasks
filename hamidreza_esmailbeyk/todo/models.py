from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


user = get_user_model()



class Todo(models.Model):
    todo_title = models.CharField(max_length=300)
    todo_content = models.TextField()
    todo_priority = models.IntegerField(default=1)
    todo_is_done = models.BooleanField()
    user = models.ForeignKey(user, on_delete=models.CASCADE,related_name="todos")
    
    
    def __str__(self):
        return f"{self.todo_title}/ Is done : {self.todo_is_done}"
    
    
    
    class Meta:
        db_table = 'todos'
        