from pyexpat import model
from django.db import models

# Create your models here.
class Coupons(models.Model):
    code = models.CharField(max_length=20,primary_key=True)
    discout = models.IntegerField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code