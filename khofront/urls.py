
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('detail/<page>-<pk>.html', views.detail, name='detail'),
    path('success', views.success_post, name='success'),
    path('register_email', views.register_email, name='email_register')
]
