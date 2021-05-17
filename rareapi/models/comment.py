from django.db import models
from django.db.models.deletion import CASCADE

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=False, auto_now=True)