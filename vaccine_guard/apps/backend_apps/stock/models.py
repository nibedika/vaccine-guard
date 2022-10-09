from django.db import models
from django import forms

from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.core.validators import URLValidator


# Create your models here.
class Table(models.Model):

	# General Info Fields
	quantity = models.IntegerField(null=True, blank=True)
	
	def __str__(self):
		return self.quantity
