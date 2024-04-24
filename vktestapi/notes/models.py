from django.db import models

# Database representation of note
class Note(models.Model):
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=5000)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.title
