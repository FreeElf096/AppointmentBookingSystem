from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class myCustomUser(AbstractUser):
	username = models.CharField(max_length=20, unique="True", blank=False)
	password = models.CharField(max_length=200)

	isPatient = models.BooleanField(default=False)
	isDoctor = models.BooleanField(default=False)

	firstName = models.CharField(max_length=200, blank=True, null=True)
	lastName = models.CharField(max_length=200, blank=True, null=True)
	email = models.EmailField(unique=True)
	dateOfBirth = models.CharField(max_length=200, blank=True, null=True)
	address = models.CharField(max_length=200, blank=True, null=True)
	contactNo = models.IntegerField(null=True, unique=True)

	def __str__(self):
		return self.firstName


class Doctor(models.Model):
	user = models.OneToOneField(myCustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='doctor_releted_user')
	degree = models.CharField(max_length=200, blank=True, null=True)
	speciality = models.CharField(max_length=200, blank=True, null=True)
	isApproved = models.BooleanField(default=False)

	def __str__(self):
		return self.user.firstName


class Patient(models.Model):
	user = models.OneToOneField(myCustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='patient_releted_user')
	gender = models.CharField(max_length=200, blank=True, null=True)


class Appointment(models.Model):
	pname = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_releted_appointment', null=True, blank=True)
	doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.CASCADE, related_name='doctor_releted_appornment')
	date = models.DateTimeField(null=True, blank=True)
	isConfiremed = models.BooleanField(default=False)