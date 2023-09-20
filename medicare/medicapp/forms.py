from .models import Profile
from django import forms
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['user','full_name','birth_date','gender']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'status', 'patient', 'doctor']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD',
                    'class': 'form-control form-control-lg',
                    'type': 'date',
                }
            ),
            'time': forms.TimeInput(
                attrs={
                    'placeholder': 'HH:MM',
                    'class': 'form-control form-control-lg',
                    'type': 'time',
                }
            ),
            'status': forms.Select(
                attrs={'class': 'form-control form-control-lg'}
            ),
            'patient': forms.Select(
                attrs={'class': 'form-control form-control-lg'}
            ),
            'doctor': forms.Select(
                attrs={'class': 'form-control form-control-lg'}
            ),
        }

from django import forms
from django.contrib.auth.models import User  # Import the User model

class CurrentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter Your First Name', 'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Your Last Name', 'id': 'last_name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Your Email', 'id': 'email'}),
            # 'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number', 'id': 'phone_number'}),
        }
