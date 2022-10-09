# Buildin Package
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q as Q_set
from package.helper import Helper as hp
from django.core.mail import send_mail

# App's Model Import
from apps.access_apps.access.models import User as userDB
from apps.backend_apps.supplier.models import Table as supplierDB


# Create your views here.
class Supplier():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg


	def add_supplier(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)

			if request.method == 'POST' and request.POST.get('supplier_add'):

				supplierId = hp.unique_custom_id(hp, 'S')

				# Data entry block start 
				data   = supplierDB(
					supplier_id = supplierId,
					name        = request.POST.get('name'),
					mobile      = request.POST.get('mobile'),
					address     = request.POST.get('address'),
				)
				status    = data.save()
				# Data entry block end 

				return redirect('all_supplier')

			elif request.method == 'GET':
				return render(request, 'supplier_add.html', {'menuData': menuInfo})

			return render(request, 'supplier_add.html', {'menuData': menuInfo})
		else:
			return redirect('home')



	def all_supplier(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			supplierWhere   = Q_set(trash=False)
			supplierInfo    = supplierDB.objects.filter(supplierWhere)

			return render(request, 'supplier_all.html', {'menuData': menuInfo, 'supplierData': supplierInfo})
		else:
			return redirect('home')



	def view_supplier(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			supplierWhere   = Q_set(id=id, trash=False)
			supplierInfo    = supplierDB.objects.get(supplierWhere)

			return render(request, 'supplier_view.html', {'menuData': menuInfo, 'supplierData': supplierInfo})
		else:
			return redirect('sign_out')



	def edit_supplier(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)

			supplierWhere   = Q_set(id=id, trash=False)
			supplierInfo    = supplierDB.objects.get(supplierWhere)

			# Update Profile Picture And Cover Picture Start Here ------------->
			if request.method == 'POST' and request.POST.get('supplier_edit'):

				# Data entry block start 
				where        = Q_set(id=id, trash=False)
				pre_update   = supplierDB.objects.select_related().filter(where)
				post_update  = pre_update.update(
					name     = request.POST.get('name'),
					mobile   = request.POST.get('mobile'),
					address  = request.POST.get('address'),
			    )
				# Data entry block end

				return redirect('all_supplier') 
			elif request.method == 'GET':
				return render(request, 'supplier_edit.html', {'menuData': menuInfo, 'supplierData': supplierInfo})
			return render(request, 'supplier_edit.html', {'menuData': menuInfo, 'supplierData': supplierInfo})
		else:
			return redirect('home')




	def delete_supplier(request, id):
		if request.session.has_key('username'):

			supplierWhere       = Q_set(id=id, trash=False)
			supplierInfo        = supplierDB.objects.get(supplierWhere)

			supplierInfo.delete()
			return redirect('all_supplier')
		else:
			return redirect('home')