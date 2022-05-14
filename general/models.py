from django.db import models

# Create your models here.
class Contact(models.Model):
    email =models.EmailField(verbose_name="email",max_length=200)
    message = models.CharField(max_length=1000)
    subject = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    contact_date = models.DateField(null=True, blank=True,)
    

    def __str__(self):
        return self.email