from django.urls import path, include
from .views import *
urlpatterns = [

    path('new', register_user, name="register"),
    path('login', user_login, name="login"),
    path('update', user_update, name="update"),
    path('add/address', create_address, name="address"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),


]
