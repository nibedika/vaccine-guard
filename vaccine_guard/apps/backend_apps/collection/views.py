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
from apps.backend_apps.collection.models import Table as collectionDB
from apps.backend_apps.stock.models import Table as stockDB


# Create your views here.
class Collection():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg


	def add_collection(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)

			supplierWhere    = Q_set(status='active', trash=False)
			supplierInfo     = supplierDB.objects.filter(supplierWhere)

			if request.method == 'POST' and request.POST.get('collection_add'):

				collectionId = hp.unique_custom_id(hp, 'C')

				supWhere = Q_set(id=request.POST.get('supplier_id'), status='active', trash=False)
				supInfo  = supplierDB.objects.get(supWhere)


				# Stock Data update block start)
				try:
					stockWhere = Q_set(id=1)
					stockInfo  = stockDB.objects.get(stockWhere)
				except:
					stockInfo  = ''

				if stockInfo != '':
					stockQty      = int(stockInfo.quantity) + int(request.POST.get('quantity'))

					pre_update    = stockDB.objects.select_related().filter(stockWhere)
					post_update   = pre_update.update(quantity = stockQty)
				else:
					data   = stockDB(quantity = request.POST.get('quantity'))
					status = data.save()
				# Stock Data update block end


				# Data entry block start 
				data   = collectionDB(
					collection_id = collectionId,
					supplier_id   = supInfo,
					quantity      = request.POST.get('quantity'),
				)
				status = data.save()
				# Data entry block end 

				return redirect('all_collection')
			elif request.method == 'GET':
				return render(request, 'collection_add.html', {'menuData': menuInfo, 'supplierData': supplierInfo})

			return render(request, 'collection_add.html', {'menuData': menuInfo, 'supplierData': supplierInfo})
		else:
			return redirect('home')



	def all_collection(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			collectionWhere = Q_set(trash=False)
			collectionInfo  = collectionDB.objects.filter(collectionWhere)

			return render(request, 'collection_all.html', {'menuData': menuInfo, 'collectionData': collectionInfo})
		else:
			return redirect('home')



	def delete_collection(request, id):
		if request.session.has_key('username'):

			collectionWhere = Q_set(id=id, trash=False)
			collectionInfo  = collectionDB.objects.get(collectionWhere)

			# Stock Data update block start
			try:
				stockWhere = Q_set(id=1)
				stockInfo  = stockDB.objects.get(stockWhere)
			except:
				stockInfo  = ''

			if stockInfo != '':
				stockQty      = int(stockInfo.quantity) - int(collectionInfo.quantity)

				pre_update    = stockDB.objects.select_related().filter(stockWhere)
				post_update   = pre_update.update(
					quantity  = stockQty,
			    )
			else:
				pass
			# Stock Data update block end

			collectionInfo.delete()
			return redirect('all_collection')
		else:
			return redirect('home')