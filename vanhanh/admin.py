from django.contrib import admin
from .models import Product, Delivery, Done_Delivery, Typeproduct, Nofication, Grouptype, Classification

# Register your models here.

admin.site.site_header = "Kho vạn hạnh"

# class ProductDescriptionInline(admin.StackedInline):
#     model = Product
#     fields = ['description']

class ClassificationView(admin.ModelAdmin):
    list_display = ['name']

class TypeproductView(admin.ModelAdmin):
    list_display= ['name', 'highlight', 'group_type']
    list_filter = ['highlight']

class GrouptypeView(admin.ModelAdmin):
    list_display = ['name', 'highlight', 'classification']
class ProductView(admin.ModelAdmin):
    list_display = ['name', 'price', 'type']
    search_fields = ['name']
    list_filter = ['type']
    # inlines = [ProductDescriptionInline]

class NoficationView(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(Classification, ClassificationView)
admin.site.register(Grouptype, GrouptypeView)
admin.site.register(Nofication,NoficationView)
admin.site.register(Product, ProductView)
admin.site.register(Delivery)
admin.site.register(Done_Delivery)
admin.site.register(Typeproduct, TypeproductView)