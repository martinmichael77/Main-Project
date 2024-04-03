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
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)  
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
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True, null=True)  # Use auto_now_add=True for initial creation


    def __str__(self):
        return f"Payment ID: {self.id}, Status: {self.payment_status}"
    

    # class PrescriptionRefillRequest(models.Model):
    #     patient = models.ForeignKey(User, related_name="refill_requests", on_delete=models.CASCADE)
    #     prescription = models.ForeignKey(Medical, related_name="refill_requests", on_delete=models.CASCADE)
    #     request_date = models.DateTimeField(auto_now_add=True)
    #     is_approved = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"Refill Request for Prescription ID: {self.prescription.id} by {self.patient.username}"

# medicapp/models.py
from django.contrib.auth.models import User
from django.db import models

class PrescriptionRefill(models.Model):
    patient = models.ForeignKey(User, related_name="refill_requests", on_delete=models.CASCADE)
    prescription = models.ForeignKey(Treatment, related_name="refill_requests", on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Refill Request for Prescription ID: {self.prescription.id} by {self.patient.username}"

# models.py
from django.db import models
from django.contrib.auth.models import User

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)  # Replace 1 with an appropriate user ID or default value
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # Assuming is_active is a BooleanField

    # Add other fields as needed

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    opening_days = models.CharField(max_length=100, null=True, blank=True)
    hospital_image = models.ImageField(upload_to='hospital_images/', null=True, blank=True)
    avgrating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserSellerDistance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    distance = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'hospital')


class Review(models.Model):
    REVIEWED = 'reviewed'
    PENDING = 'pending'
    
    REVIEW_CHOICES = [
        (REVIEWED, 'reviewed'),
        (PENDING, 'Pending'),
    ]

    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    rating = models.IntegerField()
    outof_rating = models.IntegerField(default=5, editable=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_CHOICES,
        default=PENDING,
    )


    def _str_(self):
        return f"Review by {self.user.username}"
    
class AppointmentCounselling(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"Appointment with {self.counselor.get_full_name()}"
    

from django.db import models
from django.contrib.auth.models import User


from django.db import models

class HealthcareTip(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='healthcare_tips/', null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    bookmarks_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

class LikedTip(models.Model):
    session_key = models.CharField(max_length=40)
    tip = models.ForeignKey(HealthcareTip, on_delete=models.CASCADE)

class BookmarkedTip(models.Model):
    session_key = models.CharField(max_length=40)
    tip = models.ForeignKey(HealthcareTip, on_delete=models.CASCADE)



from django.db import models
from django.contrib.auth.models import User

class HealthMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_metrics')
    timestamp = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(null=True, blank=True)  # in kilograms
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)  # systolic blood pressure (mmHg)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)  # diastolic blood pressure (mmHg)
    blood_sugar = models.FloatField(null=True, blank=True)  # blood sugar level (mg/dL)
    heart_rate = models.IntegerField(null=True, blank=True)  # heart rate (bpm)
    # Add more fields as needed

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Health Metric for {self.user.username} recorded at {self.timestamp}"



class Ambulance(models.Model):
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100)
    vehicle_capacity = models.IntegerField()
    driver_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Ambulance - {self.vehicle_number}"

