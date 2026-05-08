from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    fee = models.IntegerField()
    rating = models.FloatField(default=4.5)

    def __str__(self):
        return self.name


class DoctorAvailability(models.Model):
    DAYS_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.day}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField() 
    message = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"
    

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name