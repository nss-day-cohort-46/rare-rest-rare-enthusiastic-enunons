from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=100)
    img_url = models.CharField(max_length=255)