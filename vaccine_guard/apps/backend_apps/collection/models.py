from django.db import models
from django import forms

from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import validate_image_file_extension
from django.core.validators import URLValidator

from apps.backend_apps.supplier.models import Table as supplierDB

# Create your models here.
class Table(models.Model):

	# General Info Fields
	date           = models.DateTimeField(auto_now_add=True)
	collection_id  = models.CharField(max_length=50, blank=False)
	supplier_id    = models.ForeignKey(supplierDB, on_delete=models.CASCADE, related_name='supplier_collection')
	
	quantity       = models.IntegerField(null=True, blank=True)

	status         = models.CharField(validators=[RegexValidator], max_length=50, default='active') #option-> active, inactive

	# Backup Fields
	trash          = models.BooleanField(default=False)
	
	def __str__(self):
		return self.collection_id
