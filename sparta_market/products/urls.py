from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "products"
urlpatterns = [
    path('', views.home, name='home'),
    path('detail/', views.detail, name="detail")
]