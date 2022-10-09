from django.db import models
from django import forms

from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.core.validators import URLValidator


# Create your models here.
class Table(models.Model):

	# General Info Fields
	date        = models.DateTimeField(auto_now_add=True)
	supplier_id = models.CharField(max_length=50, blank=False)
	name        = models.CharField(max_length=50, blank=False)
	mobile      = models.CharField(max_length=50, blank=True)
	address     = models.TextField(blank=True)

	status      = models.CharField(validators=[RegexValidator], max_length=50, default='active') #option-> active, inactive

	# Backup Fields
	trash       = models.BooleanField(default=False)
	
	def __str__(self):
		return self.supplier_id
