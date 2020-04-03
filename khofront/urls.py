
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('detail/<page>-<pk>.html', views.detail, name='detail'),
    path('success', views.success_post, name='success'),
    path('register_email', views.register_email, name='email_register'),
    path("type/<page>-<pk>", views.type_product, name="type_product"),
    path("/search", views.search, name="search"),
    path("cartboard", views.cartboard, name="cartboard"),
    path("group/<page>-<pk>.html", views.group, name='group')
]
