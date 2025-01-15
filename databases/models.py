from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abilities = models.JSONField(default=list)
    types = models.JSONField(default=list)
    stats = models.JSONField(default=dict)

    def __str__(self):
        return self.name
