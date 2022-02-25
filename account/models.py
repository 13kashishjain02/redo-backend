from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
import uuid

# Create your models here.



phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class MyAccountManager(BaseUserManager):
    # create_user deals with creating the user of costumer type
    def create_user(self, email, name=None, contact_number=None, viewpass=None, password=None, ):
        if not email:
            raise ValueError("enter email")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            viewpass=viewpass,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_vendor(self, shop_number, shop_name, shop_add, plan, gst, vendor, subscripton_amount):

        user = self.model(
            shop_number=shop_number,
            shop_name=shop_name,
            shop_add=shop_add,
            plan=plan,
            gst=gst,
            vendor=vendor,
            subscripton_amount=subscripton_amount,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, contact_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            contact_number=contact_number,
            # viewpass=viewpass,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    # viewpass = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True, validators=[phone_regex])
    # order_history = models.JSONField(default=list, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_Vendor = models.BooleanField(default=False)
    is_Blogger = models.BooleanField(default=False)
    is_Affiliate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

def get_uplaod_file_name(userpic, filename,):
    return u'shop/%s/%s%s' % (str(userpic.vendor_id)+"/data","",filename)
def get_uplaod_file_name_blog(userpic, filename,):
    return u'blog/%s/%s%s' % (str(userpic.blogger_id)+"/template","",filename)

class VendorAccount(models.Model):
    vendor = models.OneToOneField(Account, default=None, on_delete=models.CASCADE, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    shop_number = models.IntegerField(null=True, blank=True)
    shop_name = models.CharField(max_length=150)
    shop_add = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    pincode = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=20)
    gst = models.CharField(max_length=30 ,null=True, blank=True)
    vat = models.CharField(max_length=30, null=True, blank=True)
    aadhaar_card = models.CharField(max_length=30, null=True, blank=True)
    pan = models.CharField(max_length=30, null=True, blank=True)
    companypan = models.CharField(max_length=30, null=True, blank=True)
    pan_image = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    aadhaar_image = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    companypan_image = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    facebook_link = models.CharField(max_length=200, null=True, blank=True)
    instagram_link = models.CharField(max_length=200, null=True, blank=True)
    twitter_link = models.CharField(max_length=200, null=True, blank=True)
    linkedin_link = models.CharField(max_length=200, null=True, blank=True)
    youtube_link = models.CharField(max_length=200, null=True, blank=True)
    # pinterest_link = models.CharField(max_length=200, null=True, blank=True)
    # pickup_address = models.CharField(max_length=200, null=True, blank=True)
    bank_account_number=models.IntegerField(null=True, blank=True)
    bank_ifsc_code = models.IntegerField(null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_account_holder_name = models.CharField(max_length=100, null=True, blank=True)
    order_list = models.JSONField(default=list, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    # vision = models.CharField(max_length=1200, null=True, blank=True)

    # objects= MyAccountManager()
    def __str__(self):
        return self.shop_name

# only has permission to make changes or view anything in django administration can change it to staff later
#     def has_perm(self, perm,obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True


class BloggerAccount(models.Model):
    # Blogger_id = models.AutoField(primary_key=True)
    blogger = models.OneToOneField(Account, default=None, on_delete=models.CASCADE, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    subscripton_amount = models.IntegerField(null=True, blank=True)
    blogname = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)















# my models

class Unique(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)


class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    gender = models.CharField(max_length=100,choices=(('Male','Male'),('Female','Female')),blank=True)
    image = models.ImageField(default='default.png',upload_to="profile")
    dob = models.DateField(verbose_name="Date of Birth",null=True)
    location = models.CharField(max_length=100,blank=True)

class Address(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    pincode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField()
    town = models.CharField(max_length=500)
    city = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.id)
