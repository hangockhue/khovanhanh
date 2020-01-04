from django.contrib import admin
from .models import Product, Order, Done_Delivery, Typeproduct, Nofication, Grouptype

# Register your models here.

admin.site.site_header = "Kho vạn hạnh"

# class ProductDescriptionInline(admin.StackedInline):
#     model = Product
#     fields = ['description']

class TypeproductView(admin.ModelAdmin):
    list_display= ['name', 'highlight', 'group_type']
    list_filter = ['highlight']

class GrouptypeView(admin.ModelAdmin):
    list_display = ['name', 'highlight']
class ProductView(admin.ModelAdmin):
    list_display = ['name', 'price', 'type']
    search_fields = ['name']
    list_filter = ['type']
    # inlines = [ProductDescriptionInline]

class NoficationView(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(Grouptype, GrouptypeView)
admin.site.register(Nofication,NoficationView)
admin.site.register(Product, ProductView)
admin.site.register(Order)
admin.site.register(Done_Delivery)
admin.site.register(Typeproduct, TypeproductView)