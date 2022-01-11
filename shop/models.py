from django.db import models
from account.models import VendorAccount,Account
from ckeditor.fields import RichTextField

# addproduct
from django.utils.text import slugify
from django.db.utils import IntegrityError
import math

# from sorl.thumbnail import ImageField, get_thumbnail
import datetime
from PIL import Image

# Create your models here.

def get_uplaod_file_name(userpic, filename, ):
    return u'shop/%s/%s%s' % (str(userpic.vendor_id) + "/products", "", filename)

def get_uplaod_file_name_variation(userpic, filename, ):
    return u'shop/%s/%s%s' % (str(userpic.product.vendor_id) + "/products", "", filename)

def get_uplaod_category(userpic, filename, ):
    return u'category/%s/%s%s' % (str(userpic.name), "", filename)

PRODUCTFOR_CHOICES = (
    ('men', 'MEN'),
    ('women', 'WOMEN'),
    ('boy', 'BOY'),
    ('girl', 'GIRL'),
    ('general', 'GENERAL'),
)
STATUS = (
    ('waiting', 'NOTPLACED'),
    ('placed', 'PLACED'),
    ('accepted', 'ACCEPTED'),
    ('packed', 'PACKED'),
    ('shipped', 'SHIPPED'),
    ('delivered', 'DELIVERED'),
)


class Category(models.Model):
    name = models.CharField(max_length=40, default="")
    image = models.ImageField(upload_to=get_uplaod_category,null=True, blank=True, )
    mobile_image = models.ImageField(upload_to=get_uplaod_category,null=True, blank=True, )
    def __str__(self):
        return self.name


class SubCategory1(models.Model):
    name = models.CharField(max_length=40, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubCategory2(models.Model):
    name = models.CharField(max_length=40, default="")
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    vendor = models.ForeignKey(VendorAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    category2 = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE, null=True, blank=True)
    subcategory2 = models.ForeignKey(SubCategory2, on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    product_for = models.CharField(max_length=7, choices=PRODUCTFOR_CHOICES, default='general')
    brand = models.CharField(max_length=50, null=True)
    tags = models.CharField(max_length=500, null=True, blank=True, default="blanktag")
    material = models.CharField(max_length=50, null=True, blank=True, default="")
    slug = models.SlugField(max_length=170, unique=True)
    sku = models.CharField(max_length=50, null=True,blank=True,unique=True)
    in_stock = models.BooleanField(default=False)
    discount = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    mrp = models.FloatField(default=60.00, null=True, blank=True)
    special_price = models.FloatField(null=True,blank=True)
    our_price = models.FloatField(null=True,blank=True)
    description = RichTextField(null=True, blank=True, )
    short_description = RichTextField(null=True, blank=True, )
    weight = models.FloatField(default=0.00, null=True)
    length= models.FloatField(default=0.00, null=True)
    width = models.FloatField(default=0.00, null=True)
    height = models.FloatField(default=0.00, null=True)
    pub_date = models.DateField(null=True, blank=True, )
    is_recycled = models.BooleanField(default=False)
    is_upcycled = models.BooleanField(default=False)
    is_ecofriendly = models.BooleanField(default=False)
    has_variation = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_uplaod_file_name,  null=True, blank=True,)
    image2 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    image3 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )

    def __str__(self):
        return self.name

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    in_stock = models.BooleanField(default=False)
    stock = models.IntegerField(null=True, blank=True)
    mrp = models.FloatField(default=60.00, null=True, blank=True)
    special_price = models.FloatField(null=True,blank=True)
    our_price = models.FloatField(null=True,blank=True)
    pub_date = models.DateField(null=True, blank=True, )
    image = models.ImageField(upload_to=get_uplaod_file_name_variation, null=True, blank=True,)
    image2 = models.ImageField(upload_to=get_uplaod_file_name_variation, null=True, blank=True, )
    image3 = models.ImageField(upload_to=get_uplaod_file_name_variation, null=True, blank=True, )

    def __str__(self):
        return self.product.name

class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    zipcode = models.IntegerField(default=00)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=20, default="")
    contact_number = models.IntegerField()
    total = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='waiting')
    date = models.DateField(null=True, blank=True,)
    order_list = models.JSONField(default=list, blank=True, null=True)
    transaction_id = models.CharField(max_length=20, default="")

    def save(self, *args, **kwargs):
        self.date = datetime.date.today()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.status

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product)
    def __str__(self):
        return self.user.name

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    cartdata = models.JSONField(default=list, blank=True, null=True)
    def __str__(self):
        return self.user.name