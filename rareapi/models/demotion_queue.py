from django.db import models

class DemotionQueue(models.Model):
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="+")
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    action = models.CharField(max_length=100)