from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from django.views.decorators.csrf import csrf_exempt
import keys
import jwt



@csrf_exempt
def splash_screen(request):
    response_json = {}
    if request.method == 'GET':
        try:
            version = int(KeysData.objects.get(key='version').value)
            print("Version " + str(version))
            compulsory_update = KeysData.objects.get(key='compulsory_update').value
            print ('compulsory_update '+str(compulsory_update))
            response_json[keys.KEY_VERSION] = version
            if int(compulsory_update) == 1:
                response_json[keys.KEY_COMPULSORY_UPDATE] = True
                print ('compulsory_update '+ "True")
            if int(compulsory_update) == 0:
                response_json['compulsory_update'] = False
                print ('compulsory_update '+ "False")
            response_json[keys.KEY_SUCCESS] = True
            response_json[keys.KEY_MESSAGE] = "SuccessFull"
        except Exception as e:
            print("Exception Error", str(e))
            response_json[keys.KEY_SUCCESS] = False
            response_json[keys.KEY_MESSAGE] = "Something went Wrong "+str(e)
    else:
        response_json[keys.KEY_SUCCESS] = False
        response_json[keys.KEY_MESSAGE] = "Not get method"
    print(response_json)
    return JsonResponse(response_json)

@csrf_exempt
def welcome_screen(request):
    response_json = {}
    if(request.method == 'GET'):
        slider_list = []
        try:        
            for o in WelcomeData.objects.all():

                welcome_details = {
                keys.KEY_ID: int(o.id),
                keys.KEY_IMAGE_URL: request.scheme + '://' + request.get_host() +"/media/"+ str(o.image),
                keys.KEY_MESSAGE: str(o.quote)
                }
                slider_list.append(welcome_details)
            response_json[keys.KEY_SUCCESS] = True
            response_json[keys.KEY_MESSAGE] = 'Success'
            response_json[keys.KEY_WELCOME_PAGE] = slider_list
        except Exception as e:
            print(e)
            response_json[keys.KEY_SUCCESS] = False
            response_json[keys.KEY_MESSAGE] = str(e)
    else:
        response_json[keys.KEY_SUCCESS] = False
        response_json[keys.KEY_MESSAGE] = "Wrong Request Method"
    print(response_json)
    return JsonResponse(response_json)
