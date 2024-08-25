from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "products"
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/detail/', views.detail, name="detail"),
    path('create/', views.create, name="create"),
    path('<int:pk>/update/', views.update, name="update"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path("<int:pk>/comments/<int:comment_pk>/delete/", views.comment_delete, name="comment_delete",),
]