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


# Create your views here.
class Appointment():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg


	def add_appointment(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			if request.method == 'POST' and request.POST.get('appointment_add'):

				# Data entry block start 
				data = appointmentDB(
					user_id         = menuInfo,
					appointment_id  = hp.unique_custom_id(hp, 'A')
				)
				status = data.save()


				# Confirmation Email Start
				subject   = 'Vaccine Appointment'
				message   = 'Your appointment have successfully taken for the Vaccine. You will be notified soon about you vaccine date. Thank you.'
				sender    = 'Vaccine Guard Org.'
				receiver  = menuInfo.email

				emailSend = send_mail(subject, message, sender, [receiver], fail_silently=False)
				# Confirmation Email End


				return redirect('add_appointment')
				# Data entry block end

			elif request.method == 'GET':
				return render(request, 'appointment_add.html', {'menuData': menuInfo})

			return render(request, 'appointment_add.html', {'menuData': menuInfo})
		else:
			return redirect('home')



	def all_appointment(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			appointmentWhere       = Q_set(trash=False)
			appointmentInfo        = appointmentDB.objects.filter(appointmentWhere)

			return render(request, 'appointment_all.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo})
		else:
			return redirect('home')



	def edit_appointment(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)

			appointmentWhere = Q_set(id=id, trash=False)
			appointmentInfo  = appointmentDB.objects.get(appointmentWhere)

			# Update Profile Picture And Cover Picture Start Here ------------->
			if request.method == 'POST' and request.POST.get('appointment_edit'):

				# Data entry block start 
				where       = Q_set(id=id, trash=False)
				pre_update  = appointmentDB.objects.select_related().filter(where)
				post_update = pre_update.update(
					status  = request.POST.get('status'),
			    )
				# Data entry block end

				return redirect('all_appointment') 
			elif request.method == 'GET':
				return render(request, 'appointment_edit.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo})
			return render(request, 'appointment_edit.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo})
		else:
			return redirect('home')



	def delete_appointment(request, id):
		if request.session.has_key('username'):

			appointmentWhere       = Q_set(id=id, trash=False)
			appointmentInfo        = appointmentDB.objects.get(appointmentWhere)

			appointmentInfo.delete()
			return redirect('all_appointment')
		else:
			return redirect('home')