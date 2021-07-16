from django.db import models
from account.models import VendorAccount,Account
from ckeditor.fields import RichTextField


# Create your models here.

def get_uplaod_file_name(userpic, filename, ):
    return u'shop/%s/%s%s' % (str(userpic.vendor_id) + "/products", "", filename)


PRODUCTFOR_CHOICES = (
    ('men', 'MEN'),
    ('women', 'WOMEN'),
    ('boy', 'BOY'),
    ('girl', 'GIRL'),
    ('general', 'GENERAL'),
)


class Category(models.Model):
    name = models.CharField(max_length=40, default="")

    def __str__(self):
        return self.name


class SubCategory1(models.Model):
    name = models.CharField(max_length=40, default="")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class SubCategory2(models.Model):
    name = models.CharField(max_length=40, default="")
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(VendorAccount, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    subcategory2 = models.ForeignKey(SubCategory2, on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    product_for = models.CharField(max_length=7, choices=PRODUCTFOR_CHOICES, default='general')
    brand = models.CharField(max_length=50, null=True)
    tags = models.CharField(max_length=500, null=True, blank=True, default="blanktag")
    slug = models.SlugField(max_length=60, unique=True)
    in_stock = models.BooleanField(default=False)
    discount = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    mrp = models.FloatField(default=60.00, null=True, blank=True)
    special_price = models.FloatField(null=True,blank=True)
    our_price = models.FloatField(null=True,blank=True)
    description = RichTextField(null=True, blank=True, )
    short_description = RichTextField(null=True, blank=True, )
    weight = models.FloatField(default=5.00, null=True)
    length= models.FloatField(default=50.00, null=True)
    width = models.FloatField(default=50.00, null=True)
    height = models.FloatField(default=50.00, null=True)
    pub_date = models.DateField(null=True, blank=True, )
    is_recycle = models.BooleanField(default=False)
    is_upcycle = models.BooleanField(default=False)
    is_ecofriendly = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_uplaod_file_name, default="")
    image2 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )
    image3 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    zipcode = models.IntegerField(default=00)
    landmark = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=20, default="")
    contact_number = models.IntegerField()
    total = models.IntegerField(null=True)
    status = models.CharField(max_length=15, default="order noted")
    order_list = models.JSONField(default=list, blank=True, null=True)
    previous_order = models.JSONField(default=list, blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.status

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    wishlist = models.ManyToManyField(Product)
    def __str__(self):
        return self.user.name

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    cartdata = models.JSONField(default=list, blank=True, null=True)
    def __str__(self):
        return self.user.name