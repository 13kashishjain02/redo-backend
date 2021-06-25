from django.db import models

# Create your models here.
class Cartdata(models.Model):
    product_id = models.IntegerField(null=True, blank=True, default=0)
    username = models.EmailField(verbose_name="email",max_length=100)
    qty=models.IntegerField(null=True, blank=True, default=0)
    size=models.CharField(max_length=5,null=True)
    

    def __str__(self):
        return self.username