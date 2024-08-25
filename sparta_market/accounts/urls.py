from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("update/", views.update, name="update"),
    path("delete/", views.delete, name="delete"),
    path("password/", views.change_password, name="change_password"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("<int:user_id>/follow/", views.follow, name="follow"),
]