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
