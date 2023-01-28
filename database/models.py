from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(to=User, null=False, blank=False, on_delete=models.CASCADE, related_name="blog_author")
    title = models.CharField(max_length=100)
    content = models.TextField()