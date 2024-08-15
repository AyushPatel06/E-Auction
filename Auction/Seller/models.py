import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import datetime
# Create your models here.
class SellerDetail(models.Model):
        SEX_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
        STATE_CHOICES = (("Ontario",'Ontario'),
            ("Alberta",'Alberta'),
            ("British Columbia",'British Columbia'),
            ("Quebec",'Quebec'),
            )
        usr = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, unique=True)
        dob = models.DateField(null = True)
        photo = models.ImageField(default='user-profile.png',upload_to='user',null=True)
        mobile = models.CharField(max_length=10,null=True, default='')
        alternate_mobile = models.CharField(max_length=10,null=True,blank=True,default='')
        address = models.TextField(default='')
        pincode = models.CharField(max_length=6, null=True, default='')
        locality = models.CharField(max_length=100, null=True, blank=True,default='')
        city = models.CharField(max_length=100, null=True, blank=True,default='')
        state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True,default='')
        sex = models.CharField(max_length=6,choices=SEX_CHOICES, null=True,default='')

class category(models.Model):
    name = models.CharField(max_length=50, default="")
    sub_Categories  = models.TextField(default="")
    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
        product_id = models.BigAutoField(primary_key=True)
        product_id2 = models.CharField(max_length=100,default='')
        seller = models.CharField(max_length=100)
        product_name = models.CharField(max_length=100)
        category = models.ForeignKey(category, default="", verbose_name="Category", on_delete=models.SET_DEFAULT, null=True)
        subcategory = models.CharField(max_length=50, default="")
        price = models.IntegerField(default=0)
        current_bid = models.IntegerField(default=0)
        winning_bid = models.IntegerField(default=0)
        winner = models.CharField(max_length=100,null=True,default="")
        total_bid = models.IntegerField(default=0)
        start = models.DateTimeField()
        end = models.DateTimeField()
        bid_date = models.DateTimeField(null=True)
        description = models.TextField()
        pub_date = models.DateField(auto_now=True)
        image1 = models.ImageField(upload_to='products', default="",null=True)
        image2 = models.ImageField(upload_to='products', default="",null=True,blank=True)
        image3 = models.ImageField(upload_to='products', default="",null=True,blank=True)
        image4 = models.ImageField(upload_to='products', default="",null=True,blank=True)
        image5 = models.ImageField(upload_to='products', default="",null=True,blank=True)
        image6 = models.ImageField(upload_to='products', default="",null=True,blank=True)

        def __str__(self):
            return f'{self.product_id}'
            
class Bid(models.Model):
    bid_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default="")

class Orders(models.Model):
        STATUS_CHOICES = (("Placed","Placed"),("Packed",'Packed'),("On Way",'On Way'),("Delivered",'Delivered'),("Cancel",'Cancel'))
        order_id = models.CharField(max_length=50,default='')
        saller = models.CharField(max_length=100,default='eauction@admin',)
        user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
        products = models.CharField(max_length=50)
        price = models.CharField(max_length=50,default='')
        payment = models.CharField(max_length=100,default='')
        status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='')
        paymentstatus = models.CharField(max_length=12,default='')
        date = models.DateTimeField(default=timezone.now)

