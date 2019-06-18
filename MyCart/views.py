from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from MyAccounts.models import UserProfile
from django.contrib.auth.models import User
from .forms import UserForm,UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from MyShop.views import home

def cart(request):
    cart = 
