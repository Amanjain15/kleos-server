import jwt
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import keys
from college.models import *


@csrf_exempt
def college_data():
	response_json = {}
	try:
		response_json[keys.KEY_COLLEGE_LIST] = []
		for o in CollegeData.objects.all():
			temp_json = str(o.name)
			response_json[keys.KEY_COLLEGE_LIST].append(temp_json)
		response_json[keys.KEY_SUCCESS] = True
		response_json[keys.KEY_MESSAGE] = "Successful"
		print(response_json)
	except Exception as e:
		print (e)
		response_json[keys.KEY_SUCCESS] = False
		response_json[keys.KEY_MESSAGE] = "College List does not exists."
		print(response_json)
	return response_json