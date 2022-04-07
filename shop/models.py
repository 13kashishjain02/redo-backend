from pyexpat import model
from django_countries.fields import CountryField
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


# class Category(models.Model):
#     name = models.CharField(max_length=40, default="")
#     image = models.ImageField(upload_to=get_uplaod_category,null=True, blank=True, )
#     mobile_image = models.ImageField(upload_to=get_uplaod_category,null=True, blank=True, )
#     def __str__(self):
#         return self.name


# class SubCategory1(models.Model):
#     name = models.CharField(max_length=40, default="")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class SubCategory2(models.Model):
#     name = models.CharField(max_length=40, default="")
#     subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))


class Product(models.Model):
    vendor = models.ForeignKey(VendorAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    subcategory1 = models.CharField(max_length=100,blank=True)
    subcategory2 = models.CharField(max_length=100,blank=True)
    subcategory3 = models.CharField(max_length=100,blank=True)
    state = models.CharField(choices=state_choices,max_length=255,default="Andhra Pradesh")
    size = models.CharField(max_length=50, null=True, blank=True)
    product_for = models.CharField(max_length=7, choices=PRODUCTFOR_CHOICES, default='general')
    brand = models.CharField(max_length=50, null=True)
    tags = models.CharField(max_length=500, null=True, blank=True, default="blanktag")
    material = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=170)
    gst = models.CharField(max_length=100,choices=(('5','5'),('12','12'),('18','18'),('28','28')))
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
    pub_date = models.DateField(auto_now_add=True)
    is_recycled = models.BooleanField(default=False)
    is_upcycled = models.BooleanField(default=False)
    is_ecofriendly = models.BooleanField(default=False)
    has_variation = models.BooleanField(default=False)
    is_handicraft = models.BooleanField(default=False)
    is_handloom = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_uplaod_file_name,  null=True, blank=True, max_length=500)
    image2 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, max_length=500 )
    image3 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, max_length=500 )
    image4 = models.ImageField(upload_to=get_uplaod_file_name, null=True, blank=True, max_length=500 )

    def __str__(self):
        return self.name

    def Weigth(self):
        weigth_kg = self.weight
        volumetric_weight = (self.length * self.width * self.height)/4000
        if weigth_kg > volumetric_weight:
            weigth = weigth_kg
        else:
            weigth = volumetric_weight
        return weigth

    def delivery_charges(self):
        weigth = self.Weigth()
        price = self.special_price
        d_charges = 0
        if weigth <= 0.5:
            if price <=200:
                d_charges = 30
            elif price >= 201 and price <=500:
                d_charges = 40
            elif price >= 501 and price <=1000:
                d_charges = 50
            elif price >= 1001:
                d_charges = 60
        
        elif weigth <= 1:
            if price <=200:
                d_charges = 40
            elif price >= 201 and price <=500:
                d_charges = 50
            elif price >= 501 and price <=1000:
                d_charges = 60
            elif price >= 1001:
                d_charges = 80

        elif weigth <= 2:
            if price <=200:
                d_charges = 50
            elif price >= 201 and price <=500:
                d_charges = 70
            elif price >= 501 and price <=1000:
                d_charges = 90
            elif price >= 1001:
                d_charges = 110

        elif weigth <= 3:
            if price <=200:
                d_charges = 70
            elif price >= 201 and price <=500:
                d_charges = 100
            elif price >= 501 and price <=1000:
                d_charges = 130
            elif price >= 1001:
                d_charges = 150

        elif weigth <= 4:
            if price <=200:
                d_charges = 90
            elif price >= 201 and price <=500:
                d_charges = 130
            elif price >= 501 and price <=1000:
                d_charges = 170
            elif price >= 1001:
                d_charges = 210
        
        elif weigth <= 5:
            if price <=200:
                d_charges = 110
            elif price >= 201 and price <=500:
                d_charges = 160
            elif price >= 501 and price <=1000:
                d_charges = 210
            elif price >= 1001:
                d_charges = 260
            
        elif weigth <= 10:
            if price <=200:
                d_charges = 200
            elif price >= 201 and price <=500:
                d_charges = 300
            elif price >= 501 and price <=1000:
                d_charges = 400
            elif price >= 1001:
                d_charges = 450

        elif weigth <= 15:
            if price <=200:
                d_charges = 0
            elif price >= 201 and price <=500:
                d_charges = 0
            elif price >= 501 and price <=1000:
                d_charges = 400
            elif price >= 1001:
                d_charges = 500
        return d_charges
    
    def sales_value(self):
        return (self.special_price*100)/(100+int(self.gst))
    
    def gst_value(self):
        return  self.special_price  - self.sales_value()

    def seller_commission(self):
        return (self.special_price*18/100)+self.delivery_charges()

    def gst_commission(self):
        return (self.seller_commission()*18/100)
    
    def tcs(self):
        return (self.sales_value()*1/100)
    
    def redopact_amount(self):
        return self.seller_commission() + self.gst_commission() + self.tcs()

    def seller_amount(self):
        return self.special_price - self.redopact_amount()


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
    image1 = models.ImageField(upload_to=get_uplaod_file_name_variation,max_length=500)
    image2 = models.ImageField(upload_to=get_uplaod_file_name_variation,max_length=500)
    image3 = models.ImageField(upload_to=get_uplaod_file_name_variation,max_length=500)
    # image4 = models.ImageField(upload_to=get_uplaod_file_name_variation)
    sku = models.CharField(max_length=50, null=True,blank=True,unique=True)

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

# class Wishlist(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     wishlist = models.ForeignKey(Product,on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.user)

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=100)
    def __str__(self):
        return self.user.name


class My_Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 


