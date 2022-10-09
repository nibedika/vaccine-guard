from django.db import models
from django import forms

from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.core.validators import URLValidator

from apps.access_apps.access.models import User as userDB

# Create your models here.

class Table(models.Model):

	# General Info Fields
	user_id          = models.ForeignKey(userDB, on_delete=models.CASCADE, related_name='appointment_user_id')
	appointment_id   = models.CharField(max_length=50, blank=False)
	appointment_date = models.DateField(auto_now_add=True)

	status           = models.CharField(validators=[RegexValidator], max_length=50, default='active') #option-> active, inactive 
	
	# Backup Fields
	trash            = models.BooleanField(default=False)
	
	def __str__(self):
		return self.appointment_id
