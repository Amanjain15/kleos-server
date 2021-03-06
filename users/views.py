from django.shortcuts import render

from .models import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from college.views import *
from sms import send_sms

import keys
import jwt
import random

# Create your views here.

@csrf_exempt
def user_sign_up(request):
	response_json={}
	if request.method == 'POST':
		try:
			name =  request.POST.get(keys.KEY_NAME)
			print name
			mobile =  str(request.POST.get(keys.KEY_MOBILE))
			print mobile
			email =  request.POST.get(keys.KEY_EMAIL)
			print email
			password=keys.KEY_DEFAULT_PASSWORD
			encoded_password = jwt.encode({keys.KEY_PASSWORD: str(password)}, keys.KEY_PASSWORD_ENCRYPTION,algorithm='HS256')
			print "Password Encoded" + encoded_password

			current_date = date.today()
			print current_date

			try:
				user_instance= UserData.objects.filter(mobile=mobile)
				if user_instance.exists() :
					user_instance = user_instance.objects.get(mobile=mobile)
					if OtpData.objects.get(user=user_instance).verified:
						print("User OTP is verified")
						response[keys.KEY_SUCCESS] = False
						response[keys.KEY_MESSAGE] = "User Already Exists. Please Login !"
					else :
						print("User OTP is not verified")
						user_instance = user_instance.objects.get(mobile=mobile)
						setattr(user_instance, 'name', name)
						setattr(user_instance, 'email', email)
						setattr(user_instance, 'password', encoded_password)
						setattr(user_instance, 'college', "")
						user_instance.save()
						otp = random.randint(1000, 9999)
						print "OTP " + otp
						message = 'Welcome to Kleos. Your One Time Password is ' + str(otp)
						send_sms(mobile, message)
						try:
							otp_instance = OtpData.objects.get(user=user_instance)
						except Exception as e:
							print str(e)

						setattr(otp_instance, 'otp', otp)
						setattr(otp_instance, 'verified', False)

						otp_instance.save()

						temp_access_token = jwt.encode({keys.KEY_ACCESS_TOKEN: str(mobile)},
														keys.KEY_TEMP_ACCESS_TOKEN_ENCRYPTION,
														algorithm='HS256')
						print(temp_access_token)

						response_json[keys.KEY_TEMP_ACCESS_TOKEN] = temp_access_token
						response_json[keys.KEY_SUCCESS] = True
						response_json[keys.KEY_MESSAGE] = "User details updated, Otp Sent."
				else:
					temp_access_token = jwt.encode({keys.KEY_ACCESS_TOKEN: str(mobile)},
													keys.KEY_TEMP_ACCESS_TOKEN_ENCRYPTION,
													algorithm='HS256')
					print(temp_access_token)
					otp = random.randint(1000, 9999)
					print "OTP " + otp
					message = 'Welcome to Kleos. Your One Time Password is ' + str(otp)
					send_sms(mobile, message)
					user_instance = UserData.objects.create(
															name=name,
															mobile=mobile,
															password=encoded_password,
															email=email,
															college="",
															)
					OtpData.objects.create(user=user_instance, otp=otp)
					response_json[keys.KEY_TEMP_ACCESS_TOKEN] = temp_access_token
					response_json[keys.KEY_SUCCESS] = True
					response_json[keys.KEY_MESSAGE] = "OTP successfully sent, Please verify OTP"

			except Exception as e:
				response[keys.KEY_SUCCESS] = False
				response[keys.KEY_MESSAGE] = "Error " + str(e)
				print str(e)
		except Exception as e:
			print str(e)
			response_json[keys.KEY_SUCCESS] = False
			response_json[keys.KEY_MESSAGE] = str(e)
	print response_json
	return JsonResponse(response_json)			

@csrf_exempt
def verify_otp(request):
	response = {}	
	if request.method == 'POST':
		try:
			access_token = request.POST.get(keys.KEY_TEMP_ACCESS_TOKEN)
			print access_token
			json1 = jwt.decode(str(access_token), keys.KEY_TEMP_ACCESS_TOKEN_ENCRYPTION, algorithms=['HS256'])
			mobile = str(json1['access_token'])
			print mobile
			otp = request.POST.get(keys.KEY_OTP)
			print otp
			user_instance = UserData.objects.get(mobile=mobile)
			if user_instance.exists():
				otp_instance = OtpData.objects.filter(user=user_instance, otp=otp)
				if otp_instance.exists():
					otp_instance = OtpData.objects.get(user=user_instance, otp=otp)
					setattr(otp_instance, 'verified', True)
					otp_instance.save()

					access_token = jwt.encode({keys.KEY_ACCESS_TOKEN: str(mobile)},
												keys.KEY_ACCESS_TOKEN_ENCRYPTION,
												algorithm='HS256')

					try:
						response_college = college_data()
						if(response_college[keys.KEY_SUCCESS]) :
							response_json[keys.KEY_COLLEGE_LIST]=response_college[keys.KEY_COLLEGE_LIST]
						else :
							print "Error in Getting College List " + response_college[keys.KEY_MESSAGE]
					except Exception as e:
						print "Error in Getting College List " + str(e) + " " + response_college[keys.KEY_MESSAGE]
					response[keys.KEY_NAME] = user_instance.name
					response[keys.KEY_ACCESS_TOKEN] = access_token
					response[keys.KEY_SUCCESS] = True
					response[keys.KEY_MESSAGE] = "Otp Verified"
				else:
					response[keys.KEY_SUCCESS] = False
					response[keys.KEY_MESSAGE] = "Invalid OTP"
			else:
				response[keys.KEY_SUCCESS] = False
				response[keys.KEY_MESSAGE] = "User does not exists"
		except Exception as e:
			response[keys.KEY_SUCCESS] = False
			response[keys.KEY_MESSAGE] = "Something went wrong" + str(e)
	print(response)
	return JsonResponse(response)


@csrf_exempt
def resend_otp(request):
	response_json = {}
	if request.method == "POST":
		try:
			access_token = request.POST.get(keys.KEY_TEMP_ACCESS_TOKEN)
			print access_token
			json1 = jwt.decode(str(access_token), keys.KEY_TEMP_ACCESS_TOKEN_ENCRYPTION, algorithms=['HS256'])
			mobile = str(json1['access_token'])
			user_instance = UserData.objects.get(mobile=mobile)

			try:
				otp = OtpData.objects.get(user=user_instance).otp
				message = 'Welcome to Kleos. Your One Time Password is ' + str(otp)
				send_sms(mobile, message)

				response_json[keys.KEY_SUCCESS] = True
				response_json[keys.KEY_MESSAGE] = "OTP sent"
			except Exception as e:
				print(e)
				response_json[keys.KEY_SUCCESS] = False
				response_json[keys.KEY_MESSAGE] = "OTP sent failed " + str(e)

		except Exception as e:
			print(e)
			response_json[keys.KEY_SUCCESS] = False
			response_json[keys.KEY_MESSAGE] = "Access Token not found" + str(e)

	print(response_json)
	return JsonResponse(response_json)

@csrf_exempt
def user_login(request):
	if request.method == 'POST':
		response = {}
		try:
			mobile = request.POST.get(keys.KEY_REQUEST_MOBILE)
			print mobile
			password = request.POST.get(keys.KEY_REQUEST_PASSWORD)
			print password
			encoded_password = jwt.encode({'password': str(password)}, keys.KEY_PASSWORD_ENCRYPTION, algorithm='HS256')
			print encoded_password
			user_instance = UserData.objects.filter(mobile=mobile, password=encoded_password)
			if user_instance.exists():
				response[keys.KEY_SUCCESS] = True
				response[keys.KEY_MESSAGE] = "Successful"
				access_token = jwt.encode({keys.KEY_JWT_ACCESS_TOKEN: str(mobile)}, keys.KEY_ACCESS_TOKEN_ENCRYPTION,
											algorithm='HS256')
				response[keys.KEY_ACCESS_TOKEN] = access_token

			else:
				response[keys.KEY_SUCCESS] = False
				response[keys.KEY_MESSAGE] = "Username and passwords does not match"
		except Exception as e:
			response[keys.KEY_SUCCESS] = False
			response[keys.KEY_MESSAGE] = "Error - " + str(e)
			print(str(e))
	print(response)
	return JsonResponse(response)

@csrf_exempt
def update_user_details(request):
	response_json = {}
	if request.method == 'POST':
		try:
			name =  request.POST.get(keys.KEY_NAME)
			print name
			college =  request.POST.get(keys.KEY_COLLEGE_NAME)
			print college
			password =  request.POST.get(keys.KEY_PASSWORD)
			print password
			access_token = request.POST.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json1 = jwt.decode(str(access_token), keys.KEY_TEMP_ACCESS_TOKEN_ENCRYPTION, algorithms=['HS256'])
			mobile = str(json1['access_token'])
			encoded_password = jwt.encode({keys.KEY_PASSWORD: str(password)}, keys.KEY_PASSWORD_ENCRYPTION,algorithm='HS256')
			print "Password Encoded" + encoded_password

			try:
				user_instance = UserData.objects.get(mobile=mobile)
				if user_instance.exists() :
					try:
						user_instance = user_instance.objects.get(mobile=mobile)
						if OtpData.objects.get(user=user_instance).verified:
							print("User OTP is verified")
							setattr(user_instance, 'name', name)
							setattr(user_instance, 'password', encoded_password)
							setattr(user_instance, 'college', college)
							user_instance.save()
							response[keys.KEY_SUCCESS] = True
							response[keys.KEY_MESSAGE] = "User Details Saved"	
						else:
							response[keys.KEY_SUCCESS] = False
							response[keys.KEY_MESSAGE] = "OTP Not Verified"		
					except Exception as e:
						response[keys.KEY_SUCCESS] = False
						response[keys.KEY_MESSAGE] = str(e)	
			except Exception as e:
				response[keys.KEY_SUCCESS] = False
				response[keys.KEY_MESSAGE] = str(e)
		except Exception as e:
			print str(e)
			response_json[keys.KEY_SUCCESS] = False
			response_json[keys.KEY_MESSAGE] = str(e)
	print response_json
	return JsonResponse(response_json)
