from django.shortcuts import render

# Create your views here.
from .models import *
from users.models import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta

from users.models import *

import keys
import jwt
import random

@csrf_exempt
def sponsor_list(request):
	response_json={}
	if request.method=='GET':
		try:
			access_token = request.GET.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json1 = jwt.decode(str(access_token), keys.KEY_ACCESS_TOKEN_ENCRYPTION, algorithms=['HS256'])
			mobile = str(json1['access_token'])
			try:
				user_instance=UserData.objects.filter(mobile=mobile)		
				if user_instance.exists():
					sponsor_data=SponsorData.objects.all()
					sponsors=[]
					for o in sponsor_data:
						temp_json={}
						temp_json[keys.KEY_SPONSOR_NAME]=o.name
						temp_json[keys.KEY_SPONSOR_CONTENT]=o.content
						temp_json[keys.KEY_SPONSOR_IMAGE]=request.scheme + '://' + request.get_host() +"/media/"+ str(o.image_url) 
						temp_json[keys.KEY_SPONSOR_URL]=o.url
						sponsors.append(temp_json)


					response_json[keys.KEY_SPONSOR_LIST] = sponsors
					response_json[keys.KEY_SUCCESS] = True
					response_json[keys.KEY_MESSAGE] = "Successful"
				else :
					response_json[keys.KEY_SUCCESS] = False
					response_json[keys.KEY_MESSAGE] = "Invalid Access Token"
			except Exception as e:
				response_json[keys.KEY_SUCCESS] = False
				response_json[keys.KEY_MESSAGE] = str(e)
		except Exception as e:
			response_json[keys.KEY_SUCCESS] = False
			response_json[keys.KEY_MESSAGE] = str(e)
	print response_json
	return JsonResponse(response_json)