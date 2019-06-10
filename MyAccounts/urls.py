from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'MyAccounts'

urlpatterns = [
    path('',views.index,name='authentication_check'),
    path(r'register/',views.register_user,name='register_user'),
    path(r'login/',views.login_user,name='login_user'),
    path(r'logout/',views.logout_user,name='logout_user'),
]
