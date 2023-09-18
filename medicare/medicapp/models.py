from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

    
class Medical(models.Model):
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)
    s4 = models.CharField(max_length=200)
    s5 = models.CharField(max_length=200)
    disease = models.CharField(max_length=200)
    medicine = models.CharField(max_length=200)
    patient = models.ForeignKey(User, related_name="patient", on_delete= models.CASCADE)
    doctor = models.ForeignKey(User, related_name="doctor", on_delete= models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease


class Treatment(models.Model):
    approved = models.BooleanField(default=False)
    time = models.CharField(max_length=200, null=True)
    patient = models.ForeignKey(User, related_name="pat", on_delete= models.CASCADE)
    doctor = models.ForeignKey(User, related_name="dor", on_delete= models.CASCADE, null=True)
    treatment_day = models.DateTimeField(null=True)
    medical = models.ForeignKey(Medical, related_name="medical", on_delete= models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Treatment ID: {self.id}"


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"



class Doctor(models.Model):
    first_name = models.CharField(max_length=100, default='') 
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(blank=True)
    license_no = models.CharField(max_length=20, default='')  
    phone = models.CharField(max_length=15, null=True)  

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


    
    



