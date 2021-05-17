from django.db import models

class Post(models.Model):
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now_add=False, auto_now=True)
    image_url = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

