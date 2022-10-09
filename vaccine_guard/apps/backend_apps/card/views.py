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
from apps.backend_apps.stock.models import Table as stockDB


# Create your views here.
class Card():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg


	def add_card(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)

			appointmentWhere = Q_set(status='active', trash=False)
			appointmentInfo  = appointmentDB.objects.filter(appointmentWhere)

			if request.method == 'POST' and request.POST.get('card_add'):

				cardId = hp.unique_custom_id(hp, 'C')

				aptWhere = Q_set(id=request.POST.get('appointment_id'), status='active', trash=False)
				aptInfo  = appointmentDB.objects.get(aptWhere)

				dayOne   = request.POST.get('dose_one_date')
				dayTwo   = request.POST.get('dose_two_date')
				dayThree = request.POST.get('dose_three_date')


				# Stock Data update block start
				try:
					stockWhere = Q_set(id=1)
					stockInfo  = stockDB.objects.get(stockWhere)
				except:
					stockInfo  = ''

				if stockInfo != '' and int(stockInfo.quantity) >= 3:
					stockQty      = int(stockInfo.quantity) - 3

					pre_update    = stockDB.objects.select_related().filter(stockWhere)
					post_update   = pre_update.update(
						quantity  = stockQty,
				    )

				    # Data entry block start 
					data   = cardDB(
						card_id         = cardId,
						appointment_id  = aptInfo,
						dose_one_date   = dayOne,
						dose_two_date   = dayTwo,
						dose_three_date = dayThree,
					)
					status    = data.save()
					# Data entry block end 

					# Confirmation Email Start
					subject   = 'Vaccine Card'
					message   = 'Your vaccine card has been created. You will get your vaccine dose schedule on your vaccine card. To download card visit our website. Thank you.'
					sender    = 'Vaccine Guard Org.'
					receiver  = aptInfo.user_id.email

					emailSend = send_mail(subject, message, sender, [receiver], fail_silently=False)
					# Confirmation Email End
				else:
					pass
				# Stock Data update block end


				return redirect('all_card')
			elif request.method == 'GET':
				return render(request, 'card_add.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo})

			return render(request, 'card_add.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo})
		else:
			return redirect('home')



	def all_card(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			cardWhere       = Q_set(trash=False)
			cardInfo        = cardDB.objects.filter(cardWhere)

			return render(request, 'card_all.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return redirect('home')



	def view_card(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			cardWhere       = Q_set(id=id, trash=False)
			cardInfo        = cardDB.objects.get(cardWhere)

			return render(request, 'card_view.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return redirect('sign_out')



	def view_user_card(request, id):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			appointmentWhere = Q_set(user_id=id, trash=False)
			appointmentInfo  = appointmentDB.objects.get(appointmentWhere)

			cardWhere       = Q_set(appointment_id=appointmentInfo, trash=False)
			cardInfo        = cardDB.objects.get(cardWhere)

			return render(request, 'user_card_view.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return redirect('user_sign_out')



	def edit_card(request, id):
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
			if request.method == 'POST' and request.POST.get('card_edit'):

				# Data entry block start 
				where        = Q_set(id=id, trash=False)
				pre_update   = cardDB.objects.select_related().filter(where)
				post_update  = pre_update.update(
					dose_one_date   = request.POST.get('dose_one_date'),
					dose_two_date   = request.POST.get('dose_two_date'),
					dose_three_date = request.POST.get('dose_three_date'),
			    )
				# Data entry block end


				# Confirmation Email Start
				subject   = 'Vaccine Card'
				message   = 'Your vaccine dose date has been updated. You will get your new vaccine dose schedule on your updated vaccine card. To download new card visit our website. Thank you.'
				sender    = 'Vaccine Guard Org.'
				receiver  = cardInfo.appointment_id.user_id.email

				emailSend = send_mail(subject, message, sender, [receiver], fail_silently=False)
				# Confirmation Email End


				return redirect('all_card') 
			elif request.method == 'GET':
				return render(request, 'card_edit.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo, 'cardData': cardInfo})
			return render(request, 'card_edit.html', {'menuData': menuInfo, 'appointmentData': appointmentInfo, 'cardData': cardInfo})
		else:
			return redirect('home')




	def delete_card(request, id):
		if request.session.has_key('username'):

			cardWhere       = Q_set(id=id, trash=False)
			cardInfo        = cardDB.objects.get(cardWhere)


			# Stock Data update block start
			try:
				stockWhere  = Q_set(id=1)
				stockInfo   = stockDB.objects.get(stockWhere)
			except:
				stockInfo   = ''

			if stockInfo   != '':
				stockQty    = int(stockInfo.quantity) + 3

				pre_update  = stockDB.objects.select_related().filter(stockWhere)
				post_update = pre_update.update(quantity = stockQty)
			else:
				data   = stockDB(quantity = 3)
				status = data.save()
			# Stock Data update block end


			cardInfo.delete()
			
			return redirect('all_card')
		else:
			return redirect('home')