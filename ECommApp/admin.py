from django.contrib import admin
from.models import Product,CartItem,Order
# Register your models here.
class AdimnProduct(admin.ModelAdmin):
    list_display=('product_id','product_name','category','price','proImage')

admin.site.register(Product,AdimnProduct)    

class CartItemAdmin(admin.ModelAdmin):
    list_display=('product_id','quantity','date_added') 
admin.site.register(CartItem,CartItemAdmin)


class OrdermAdmin(admin.ModelAdmin):
    list_display=('order_id','product','quantity','user','date_added','is_completed') 
admin.site.register(Order,OrdermAdmin)