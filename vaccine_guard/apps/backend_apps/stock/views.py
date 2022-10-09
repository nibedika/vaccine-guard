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
from apps.backend_apps.stock.models import Table as stockDB


# Create your views here.
class Stock():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg



	def stock(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			try:
				stockWhere = Q_set(id=1)
				stockInfo  = stockDB.objects.get(stockWhere).quantity
			except:
				stockInfo = 0

			return render(request, 'stock.html', {'menuData': menuInfo, 'stockData': stockInfo})
		else:
			return redirect('home')
