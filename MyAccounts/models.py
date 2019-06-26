from django.db import models
from django.contrib.auth.decorators import login_required

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfile(models.Model):

    def check_phoneno(value):
        if value>9999999999 or value<1000000000:
            raise ValidationError("Enter valid mobile no. !!!")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.IntegerField(validators = [check_phoneno])
    profile_pic = models.ImageField(upload_to='MyAccounts/profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
