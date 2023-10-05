from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from datetime import date, datetime


class Medical(models.Model):
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)
    s4 = models.CharField(max_length=200)
    s5 = models.CharField(max_length=200)
    disease = models.CharField(max_length=200)
    medicine = models.CharField(max_length=200)
    patient = models.ForeignKey(User, related_name="medical_records", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="treated_patients", on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease

class Treatment(models.Model):
    approved = models.BooleanField(default=False)
    time = models.CharField(max_length=200, null=True)
    patient = models.ForeignKey(User, related_name="treatments_received", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="treatments_given", on_delete=models.CASCADE, null=True)
    treatment_day = models.DateTimeField(null=True)
    medical = models.ForeignKey(Medical, related_name="treatments", on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Treatment ID: {self.id}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # @property
    # def age(self):
    #     if self.birth_date:
    #         today = date.today()
    #         age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    #         return age
    #     return None

    def __str__(self):
        return f"Profile for {self.user.username}"

class Doctor(models.Model):
    user = models.OneToOneField(User, related_name="doctor_profile", on_delete=models.CASCADE, null=True)
    license_no = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=15, null=True)
    specialization = models.CharField(max_length=255, null=True)  # Add specialization field
    is_active = models.BooleanField(default=True)

    def get_full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return "Unknown"

    def __str__(self):
        return self.get_full_name()




class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)  # Define your roles appropriately, e.g., 'admin', 'user', 'manager', etc.

    def _str_(self):
        return self.user.username
    

from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]

    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    patient = models.ForeignKey(User, related_name="appointments", on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, related_name="appointments", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.get_full_name()} for {self.patient.get_full_name()} on {self.date} at {self.time}"

    class Meta:
        ordering = ['-created_on']



from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=1)
    payment_date = models.DateTimeField(auto_now_add=True, null=True)  # Use auto_now_add=True for initial creation


    def __str__(self):
        return f"Payment ID: {self.id}, Status: {self.payment_status}"