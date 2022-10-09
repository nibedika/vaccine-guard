from django.db import models
from django import forms

from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.core.validators import URLValidator

# Create your models here.

class User(models.Model):

	# General Info Fields
	date               = models.DateTimeField(auto_now_add=True)
	user_id            = models.CharField(max_length=50, blank=False)
	name               = models.CharField(max_length=50, blank=False)
	mobile             = models.CharField(max_length=50, blank=True)
	gender             = models.CharField(max_length=50, blank=True)
	birth_date         = models.DateField(auto_now_add=False, blank=True)
	username           = models.SlugField(validators=[RegexValidator], max_length=50, blank=False)
	email              = models.EmailField(validators=[EmailValidator], max_length=100, blank=False)
	password           = models.CharField(validators=[RegexValidator], max_length=255, blank=False)
	confirmed_pass     = models.CharField(validators=[RegexValidator], max_length=255, blank=False)
	designation        = models.SlugField(validators=[RegexValidator], max_length=50, blank=False)
	profile_picture    = models.ImageField(height_field=None, width_field=None, max_length=100, blank=True)
	status             = models.CharField(validators=[RegexValidator], max_length=50, default='active') #option-> active, inactive 
	
	# Backup Fields
	trash              = models.BooleanField(default=False)
	
	def __str__(self):
		return self.user_id
