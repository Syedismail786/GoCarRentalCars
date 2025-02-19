from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Booking


# Registration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Login form
class UserLoginForm(AuthenticationForm):
    pass

# Booking form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'rental_date', 'return_date']
