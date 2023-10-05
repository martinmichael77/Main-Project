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

# class AppointmentForm(forms.ModelForm):
#     SPECIALIZATION_CHOICES = [
#         ('Dermatologists', 'Dermatologists'),
#         ('Allergists', 'Allergists'),
#         ('Diabetologists', 'Diabetologists'),
#         ('Infectious Disease Specialists', 'Infectious Disease Specialists'),
#         ('Neurologists', 'Neurologists'),
#         ('Gastroenterologists', 'Gastroenterologists'),
#         ('Urologists', 'Urologists'),
#         ('HIV Specialists', 'HIV Specialists'),
#     ]

#     # Add the specialization field using ChoiceField
#     specialization = forms.ChoiceField(
#         choices=SPECIALIZATION_CHOICES,
#         required=False,  # Set to False if you want it to be optional
#         widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
#     )
#     class Meta:
#         model = Appointment
#         fields = ['date', 'time', 'patient','specialization', 'doctor']
#         widgets = {
#             'date': forms.DateInput(
#                 attrs={
#                     'placeholder': 'YYYY-MM-DD',
#                     'class': 'form-control form-control-lg',
#                     'type': 'date',
#                 }
#             ),
#             'time': forms.TimeInput(
#                 attrs={
#                     'placeholder': 'HH:MM',
#                     'class': 'form-control form-control-lg',
#                     'type': 'time',
#                 }
#             ),
#             'patient': forms.TextInput(
#                 attrs={
#                     'class': 'form-control form-control-lg',
#                     'readonly': True,
#                 }
#             ),
#             # 'specialization': forms.TextInput(
#             #     attrs={
#             #         'class': 'form-control form-control-lg'
#             #         }
#             # ),
#             'doctor': forms.Select(
#                 attrs={'class': 'form-control form-control-lg'}
#             ),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if user:
#             self.fields['patient'].initial = user






