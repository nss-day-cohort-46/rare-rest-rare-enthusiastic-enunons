from django.db import models
from django.db.models.fields.related import ManyToManyField


class Post(models.Model):
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        "Category", on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now_add=False, auto_now=True)
    image_url = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        "Tag", through="PostTag", related_name="tags")

    @property
    def tags(self):
        return self.tags

    @tags.setter
    def tags(self, value):
        self.tags = value
