from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'MyShop'

urlpatterns = [
    path('',views.home,name='home'),
    path(r'details/<int:pid>/',views.details,name='details'),
    path(r'category/<str:Category>/',views.category,name='category'),
    path(r'cart/',views.view_cart,name='cart'),
    path(r'add_to_cart/<int:id>/<int:quant>/',views.add_to_cart,name='add_to_cart'),
    path(r'remove_from_cart/<int:id>/',views.remove_from_cart,name='remove_from_cart')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
