from django.contrib import admin
from .models import category, SellerDetail, Product, Orders
# Register your models here.
admin.site.register(category)
admin.site.register(SellerDetail)
admin.site.register(Product)
admin.site.register(Orders)