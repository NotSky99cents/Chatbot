from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Intent(models.Model):
    name= models.CharField(max_length=100, unique=True)
    response = models.TextField(max_length=500)
    tags = models.CharField(max_length=100, null=True, blank=True, unique=True)
    contexts = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Pattern(models.Model):
    question = models.CharField(max_length=255, null=True, blank=True)
    intents = models.ForeignKey(Intent, on_delete=models.CASCADE)

    def __str__(self):
        return self.question