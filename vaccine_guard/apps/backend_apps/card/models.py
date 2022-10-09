from django.db import models
from django import forms

from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.core.validators import URLValidator

from apps.backend_apps.appointment.models import Table as appointmentDB

# Create your models here.
class Table(models.Model):

	# General Info Fields
	date              = models.DateTimeField(auto_now_add=True)
	card_id           = models.CharField(max_length=50, blank=False)
	appointment_id    = models.ForeignKey(appointmentDB, on_delete=models.CASCADE, related_name='appointment_card')
	
	dose_one_date     = models.DateField(auto_now_add=False)
	dose_one_status   = models.CharField(validators=[RegexValidator], max_length=50, default='pending') #option-> pending, done
	dose_two_date     = models.DateField(auto_now_add=False)
	dose_two_status   = models.CharField(validators=[RegexValidator], max_length=50, default='pending') #option-> pending, done
	dose_three_date   = models.DateField(auto_now_add=False)
	dose_three_status = models.CharField(validators=[RegexValidator], max_length=50, default='pending') #option-> pending, done

	# Backup Fields
	trash             = models.BooleanField(default=False)
	
	def __str__(self):
		return self.card_id
