from django.db import models
from django.contrib.auth.models import User
from httpx import options
from django.utils import timezone
# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    def __str__(self):
        return self.title    
class Meta:
            verbose_name = "notes"
            verbose_name_plural = "notes"
class HomeWork(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    subject=models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateField()
    is_finished =models.BooleanField(default=False)
    def __str__(self):
       return self.title
class Todo (models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished=models.BooleanField(default=False)
    due = models.DateTimeField(default=timezone.now,null=True)
    def __str__(self):
        return self.title
class User(models.Model):
    uid = models.UUIDField(
        default=None,
        blank=True,
        null=True,
        unique=True,
    )
    USERNAME_FIELD = "uid"
    username  =models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)