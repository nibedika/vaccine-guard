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
from apps.backend_apps.appointment.models import Table as appointmentDB
from apps.backend_apps.card.models import Table as cardDB


# Create your views here.
class Vaccine():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg



	def all_vaccine(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			cardWhere       = Q_set(trash=False)
			cardInfo        = cardDB.objects.filter(cardWhere)

			return render(request, 'vaccine_all.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return redirect('home')



	def view_vaccine(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			cardWhere       = Q_set(id=id, trash=False)
			cardInfo        = cardDB.objects.get(cardWhere)

			return render(request, 'vaccine_view.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return redirect('sign_out')



	def view_user_vaccine(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			appointmentWhere = Q_set(user_id=id, trash=False)
			appointmentInfo  = appointmentDB.objects.get(appointmentWhere)

			cardWhere       = Q_set(appointment_id=appointmentInfo, trash=False)
			cardInfo        = cardDB.objects.get(cardWhere)

			return render(request, 'user_vaccine_view.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return redirect('sign_out')



	def edit_vaccine(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)

			appointmentWhere = Q_set(status='active', trash=False)
			appointmentInfo  = appointmentDB.objects.filter(appointmentWhere)
			
			cardWhere        = Q_set(id=id, trash=False)
			cardInfo         = cardDB.objects.get(cardWhere)

			# Update Profile Picture And Cover Picture Start Here ------------->
			if request.method == 'POST' and request.POST.get('vaccine_edit'):

				# Data entry block start 
				where        = Q_set(id=id, trash=False)
				pre_update   = cardDB.objects.select_related().filter(where)
				post_update  = pre_update.update(
					dose_one_status   = request.POST.get('dose_one_status'),
					dose_two_status   = request.POST.get('dose_two_status'),
					dose_three_status = request.POST.get('dose_three_status'),
			    )
				# Data entry block end


				# Confirmation Email Start
				subject   = 'Vaccine Dose'
				message   = 'Congrats for your new dose ! Hope you are feeling well. To download vaccine certificate visit our website. Thank you.'
				sender    = 'Vaccine Guard Org.'
				receiver  = cardInfo.appointment_id.user_id.email

				emailSend = send_mail(subject, message, sender, [receiver], fail_silently=False)
				# Confirmation Email End


				return redirect('all_vaccine') 
			elif request.method == 'GET':
				return render(request, 'vaccine_edit.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo, 'cardData': cardInfo})
			return render(request, 'vaccine_edit.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo, 'cardData': cardInfo})
		else:
			return redirect('home')
