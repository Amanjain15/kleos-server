from django.shortcuts import render

# Create your views here.
from .models import *
from users.models import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta

import keys
import jwt
import random


@csrf_exempt
def tab_list(request):
	response_json={}
	if request.method == 'GET' :
		try:
			access_token = request.GET.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json1 = jwt.decode(str(access_token), keys.KEY_ACCESS_TOKEN_ENCRYPTION, algorithms=['HS256'])
			mobile = str(json1['access_token'])
			try:
				user_instance=UserData.objects.filter(mobile=mobile)
				queryset = TabData.objects.order_by('position')
				print queryset.count()
				
				if user_instance.exists():
					response_json[keys.KEY_TAB_LIST] = []
					for o in queryset:
						temp_json ={ keys.KEY_TAB_TITLE : str(o.title),keys.KEY_TAB_POSITION : int(o.position),
									keys.KEY_TAB_ID : int(o.tab_id)}
						response_json[keys.KEY_TAB_LIST].append(temp_json)
					response_json[keys.KEY_SUCCESS] = True
					response_json[keys.KEY_MESSAGE] = "Successful"
				else :
					response_json[keys.KEY_SUCCESS] = False
					response_json[keys.KEY_MESSAGE] = "Invalid Access Token"
			except Exception as e:
				response_json[keys.KEY_SUCCESS] = False
				response_json[keys.KEY_MESSAGE] = str(e)
				raise
		except Exception as e:
			response_json[keys.KEY_SUCCESS] = False
			response_json[keys.KEY_MESSAGE] = str(e)
	print response_json
	return JsonResponse(response_json)