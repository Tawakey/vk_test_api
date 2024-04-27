from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import User




# Database representation of note
class Note(models.Model):
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=5000)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)


    def __str__(self):
        return self.title
