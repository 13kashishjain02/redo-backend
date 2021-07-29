from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


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
    viewpass = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True, default=00000)
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
    vendor = models.OneToOneField(Account, default=None, on_delete=models.DO_NOTHING, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    shop_number = models.IntegerField(null=True, blank=True)
    shop_name = models.CharField(max_length=150)
    shop_add = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    gst = models.CharField(max_length=30 ,null=True, blank=True)
    vat = models.CharField(max_length=30, null=True, blank=True)
    adhar_card = models.CharField(max_length=30, null=True, blank=True)
    pan = models.CharField(max_length=30, null=True, blank=True)
    pan_image = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    adhar_image = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    bank_account_number=models.IntegerField(null=True, blank=True)
    bank_ifsc_code = models.IntegerField(null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_account_holder_name = models.CharField(max_length=60, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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
    blogger = models.OneToOneField(Account, default=None, on_delete=models.DO_NOTHING, primary_key=True, )
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