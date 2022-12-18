from django.db import models

class ScrapingSettings(models.Model):
    feature = models.CharField(max_length=100)
    enable = models.BooleanField(default=False)