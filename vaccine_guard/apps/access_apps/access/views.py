# Buildin Package
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from package.helper import Helper as hp
from django.db.models import Q as Q_set
import time
from django.core.mail import send_mail

# App's Model Import
from apps.access_apps.access.models import User as userDB
from apps.backend_apps.appointment.models import Table as appointmentDB
from apps.backend_apps.card.models import Table as cardDB


# Create your views here.
class Access():

	def __init__(self, arg):
		super(self).__init__()
		self.arg = arg


	def sign_up(request):
		if request.method == 'POST' and request.POST.get('sign_up'):

			data = userDB(
				user_id        = hp.unique_custom_id(hp, 'U'),
				name           = request.POST.get('name'),
				username       = request.POST.get('username'),
				email          = request.POST.get('email'),
				password       = request.POST.get('password'),
				confirmed_pass = request.POST.get('confirmed_pass'),
				designation    = 'admin',
			)

			# Username and Email existance check start
			username     = request.POST.get('username')
			email        = request.POST.get('email')
			usernameCond = Q_set(username=username)
			usernameCond = Q_set(email=email)

			usernameExists = False
			emailExists    = False

			if userDB.objects.filter(usernameCond).exists():
				usernameExists = True
			else:
				usernameExists = False

			if userDB.objects.filter(usernameCond).exists():
				emailExists = True
			else:
				emailExists = False

			if usernameExists == False and emailExists == False:
				status = data.save()
				return redirect('sign_in')
			else:
				pass

		elif request.method == 'GET':
			return render(request, 'sign_up.html')
		return render(request, 'sign_up.html')



	def sign_in(request):
		if request.method == 'POST' and request.POST.get('sign_in'):
			loginUsername = request.POST.get('username')
			loginPassword = request.POST.get('password')

			userWhere     = Q_set(username=loginUsername)

			userExixtance = True
			if userDB.objects.filter(userWhere).exists():
				usernameExists = True
			else:
				usernameExists = True

			if userExixtance == True:
				where    = Q_set(username=loginUsername)
				userInfo = userDB.objects.filter(where)

				if userInfo[0].username == loginUsername and userInfo[0].confirmed_pass == loginPassword:
					request.session['username'] = loginUsername
					return redirect('home')
				else:
					return redirect('sign_up')
			else:
				return redirect('sign_up')
		elif request.method == 'GET':
			return render(request, 'sign_in.html')



	def user_sign_up(request):
		if request.method == 'POST' and request.POST.get('sign_up'):

			data = userDB(
				user_id        = hp.unique_custom_id(hp, 'U'),
				name           = request.POST.get('name'),
				mobile         = request.POST.get('mobile'),
				gender         = request.POST.get('gender'),
				birth_date     = request.POST.get('birth_date'),
				username       = request.POST.get('username'),
				email          = request.POST.get('email'),
				password       = request.POST.get('password'),
				confirmed_pass = request.POST.get('confirmed_pass'),
				designation    = 'user',
				status         = 'inactive',
			)

			# Username and Email existance check start
			username     = request.POST.get('username')
			email        = request.POST.get('email')
			usernameCond = Q_set(username=username)
			usernameCond = Q_set(email=email)

			usernameExists = False
			emailExists    = False

			if userDB.objects.filter(usernameCond).exists():
				usernameExists = True
			else:
				usernameExists = False

			if userDB.objects.filter(usernameCond).exists():
				emailExists = True
			else:
				emailExists = False

			if usernameExists == False and emailExists == False:

				# Confirmation Email Start\
				miliTime = int(round(time.time() * 1000))

				emailCode = str(miliTime)
				subject   = 'Email Verification'
				message   = 'Your email verification code is  - ' + emailCode
				sender    = 'Vaccine Guard Org.'
				receiver  = email

				emailSend = send_mail(subject, message, sender, [receiver], fail_silently=False)
				# Confirmation Email End

				status = data.save()
				return redirect('user_confirmation', emailCode=emailCode, email=email)
			else:
				pass

		elif request.method == 'GET':
			return render(request, 'user_sign_up.html')
		return render(request, 'user_sign_up.html')



	def user_confirmation(request, emailCode, email):

		if request.method == 'POST' and request.POST.get('user_confirmation') and emailCode != None  and email != None:

			# Identity Verification check start
			email_code = request.POST.get('email_code')
			# Identity Verification check end

			# Data update block start 
			if emailCode == email_code:
				where       = Q_set(email=email, status='inactive', trash=False)
				pre_update  = userDB.objects.select_related().filter(where)
				post_update = pre_update.update(
					status = 'active'
				)

				return redirect('user_sign_in')
			else:
				pass
			# Data update block end 

		elif request.method == 'GET':
			return render(request, 'user_confirmation.html')

		return render(request, 'user_confirmation.html')



	def user_sign_in(request):
		if request.method == 'POST' and request.POST.get('sign_in'):
			loginUsername = request.POST.get('username')
			loginPassword = request.POST.get('password')

			userWhere     = Q_set(username=loginUsername, status='active')

			userExixtance = True
			if userDB.objects.filter(userWhere).exists():
				usernameExists = True
			else:
				usernameExists = True

			if userExixtance == True:
				where    = Q_set(username=loginUsername)
				userInfo = userDB.objects.filter(where)

				if userInfo[0].username == loginUsername and userInfo[0].confirmed_pass == loginPassword:
					request.session['username'] = loginUsername
					return redirect('website')
				else:
					return redirect('user_sign_up')
			else:
				return redirect('user_sign_up')
		elif request.method == 'GET':
			return render(request, 'user_sign_in.html')



	def home(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)
			
			cardWhere      = Q_set(trash=False)
			cardInfo       = cardDB.objects.filter(cardWhere)
			card           = cardDB.objects.filter(cardWhere).count()
			
			appointmentWhere = Q_set(status='active', trash=False)
			appointmentInfo  = appointmentDB.objects.filter(appointmentWhere)
			appointment      = appointmentDB.objects.filter(appointmentWhere).count()

			return render(request, 'home.html', {'menuData': menuInfo, 'cardData': cardInfo, 'card': card, 'appointment': appointment})
		else:
			return redirect('sign_out')



	def website(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername  = request.session['username']
			userWhere        = Q_set(username=sessionUsername)
			menuInfo         = userDB.objects.get(userWhere)
			
			try:
				appointmentWhere = Q_set(user_id=menuInfo, status='active', trash=False)
				appointmentInfo  = appointmentDB.objects.get(appointmentWhere)
				
				cardWhere        = Q_set(appointment_id=appointmentInfo, trash=False)
				cardInfo         = cardDB.objects.get(cardWhere)
			except:
				cardInfo         = ''

			return render(request, 'website.html', {'menuData': menuInfo, 'cardData': cardInfo})
		else:
			return render(request, 'website.html')



	def sign_out(request):
		if request.session.has_key('username'):
			try:
				sessionUsername = request.session['username']
				userWhere       = Q_set(username=sessionUsername)
				menuInfo        = userDB.objects.get(userWhere)

				del request.session['username']
				return redirect('sign_out')
			except:
				pass
		else:
			return redirect('sign_in')
		return render(request, 'sign_in.html')



	def user_sign_out(request):
		if request.session.has_key('username'):
			try:
				sessionUsername = request.session['username']
				userWhere       = Q_set(username=sessionUsername)
				menuInfo        = userDB.objects.get(userWhere)

				del request.session['username']
				return redirect('user_sign_out')
			except:
				pass
		else:
			return redirect('user_sign_in')
		return render(request, 'user_sign_in.html')



	def view_profile(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			return render(request, 'view_profile.html', {'menuData': menuInfo})
		else:
			return redirect('sign_out')



	def edit_profile(request):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			# Update Profile Picture And Cover Picture Start Here ------------->
			if request.method == 'POST' and request.POST.get('edit_profile'):

				username = request.session['username']

				if request.FILES.get('profile_picture') != None and request.FILES.get('profile_picture') != '':
					profileImage = hp.file_processor(hp, request.FILES.get('profile_picture'), 'pro_pic', 'profile_img/')
				else:
					profileImage = menuInfo.profile_picture

				# Data entry block start 
				where  = Q_set(username=username)
				pre_update = userDB.objects.select_related().filter(where)
				post_update = pre_update.update(
					name            = request.POST.get('name'),
					password        = request.POST.get('password'),
					confirmed_pass  = request.POST.get('confirmed_pass'),
					designation     = request.POST.get('designation'),
					profile_picture = profileImage
			    )
				# Data entry block end 

				return redirect('view_profile')
			elif request.method == 'GET':
				return render(request, 'edit_profile.html', {'menuData': menuInfo})
			# Update Profile Picture And Cover Picture End Here --------------->

			return render(request, 'edit_profile.html', {'menuData': menuInfo})
		else:
			return redirect('sign_out')



	def delete_profile(request, reUser):
		if request.session.has_key('username'):

			# COMMON INFO FETCHING START
			sessionUsername = request.session['username']
			userWhere       = Q_set(username=sessionUsername)
			menuInfo        = userDB.objects.get(userWhere)

			menuInfo.delete()
			return redirect('sign_out')
		else:
			return redirect('sign_out')
