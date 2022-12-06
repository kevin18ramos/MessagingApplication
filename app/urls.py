from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name = "login"),
    path("register/", views.registerPage, name = "register"),
    path("logout/", views.logoutUser, name = "logout"),


    path("", views.home, name = "home"),
    path("send_message", views.send_message, name = "send_message"),
    
    path("send_channel_message", views.send_channel_message, name = "send_channel_message"),
    path("message_dm/<str:pk>", views.message_dm, name = "message_dm"),

    path("update_message/<str:pk>", views.update_message,name = "update_message"),
    path("delete_message/<str:pk>", views.delete_message,name = "delete_message"),

     path("delete_user/<str:pk>", views.delete_user,name = "delete_user"),
]

