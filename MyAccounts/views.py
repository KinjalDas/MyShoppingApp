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

def index(request,registered=False,user=None):
    return render(request,'MyAccounts/authentication_check.html',{'registered':registered,'user':user})

@login_required
def logout_user(request):
    # Log out the user.
    print("logout eneterd")
    if (request.session.has_key('username') or request.session.has_key('password')):
        del request.session['username']
        del request.session['password']
    logout(request)
    # Return to homepage.
    print("logout succesful")
    return home(request)

def register_user(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    if (registered == False):
        return render(request,'MyAccounts/register_user.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
    else:
        request.session['username']=user.username
        print(user.username)
        request.session['password']=user.password
        return login_user(request)

def login_user(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                request.session['username']=username
                request.session['password']=password
                return home(request,True,user)
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    elif (request.session.has_key('username') or request.session.has_key('password')):
        user = authenticate(username=request.session['username'], password=request.session['password'])

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return home(request,True,user)
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
    else:
        #Nothing has been provided for username or password.
        return render(request, 'MyAccounts/login_user.html', {})
