from django.shortcuts import render

from .models import *

from users.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from college.views import *
from users.views import *
from sms import send_sms


import keys
import jwt
import random

# Create your views here.

@csrf_exempt
def unsolved_question(access_token):
	print "unsolved_question_method"
	response={}
	try:
		json = jwt.decode(str(access_token), keys.KEY_ACCESS_TOKEN_ENCRYPTION, algorithms=['HS256'])
		mobile =str(json[keys.KEY_ACCESS_TOKEN])
		try:
			user_instance = UserData.objects.filter(mobile=mobile)
			if user_instance.exists():
				user_instance = UserData.objects.get(mobile=mobile)
				try:
					question_set=QuestionData.objects.all()
					print question_set
					try:
						print "last_question_answered"					
						last_question_answered=user_instance.last_question_answered
						print last_question_answered
						if last_question_answered > 0:
							question_data = QuestionData.objects.get(question_no=last_question_answered) 					
							user_question_data = UserQuestionData.objects.get(question=question_data,user=user_instance)
							if user_question_data.answered:
								if last_question_answered == 0:
									response[keys.KEY_NEXT_QUESTION] = QuestionData.objects.get(question_no=1).question_no
								elif last_question_answered == question_set.count() :
									response[keys.KEY_SUCCESS]=False
									response[keys.KEY_MESSAGE]="All Questions Solved"
									print response
									return response
								else :
									response[keys.KEY_NEXT_QUESTION] = QuestionData.objects.get(question_no=last_question_answered+1).question_no
								
								response[keys.KEY_SUCCESS]=True
								response[keys.KEY_MESSAGE]="Question No "+str(response[keys.KEY_NEXT_QUESTION]) 
							else :
								response[keys.KEY_SUCCESS]=False
								response[keys.KEY_MESSAGE]="Zero Questions Answered"
						else :
							print "last_question_answered "+str(last_question_answered)
							response[keys.KEY_NEXT_QUESTION] = QuestionData.objects.get(question_no=1).question_no
							response[keys.KEY_SUCCESS]=True
							response[keys.KEY_MESSAGE]="Lets Start"  					
					except Exception as e:
						print "except" + str(e)
						if "object has no attribute 'last_question_answered'" in str(e):
							response[keys.KEY_NEXT_QUESTION] = QuestionData.objects.get(question_no=1).question_no
							response[keys.KEY_SUCCESS]=True
							response[keys.KEY_MESSAGE]="Lets Start"  
						else:
							response[keys.KEY_SUCCESS]=False
							response[keys.KEY_MESSAGE]="Error "+str(e)  
				except Exception as e:
					response[keys.KEY_SUCCESS]=False
					response[keys.KEY_MESSAGE]="Error Finding Question Data "+str(e)  
			else :
				response[keys.KEY_SUCCESS]=False
				response[keys.KEY_MESSAGE]="Invalid User "				
		except Exception as e:
			response[keys.KEY_SUCCESS]=False
			response[keys.KEY_MESSAGE]="Error finding UserInstance "+str(e)
	except Exception as e:
		response[keys.KEY_SUCCESS]=False
		response[keys.KEY_MESSAGE]="Decoding Error "+str(e)
	print response
	return response

@csrf_exempt
def question_data(request,question_no):
	print str(question_no) + " question_data_method"
	response={}
	try:
		temp_json={}
		question = QuestionData.objects.get(question_no=question_no)
		temp_json[keys.KEY_QUESTION_NAME]=question.name
		temp_json[keys.KEY_QUESTION_NO]=question.question_no
		temp_json[keys.KEY_QUESTION_CONTENT]=question.content
		try:
			question_img_data = QuestionImageData.objects.get(question=question)
			temp_json[keys.KEY_QUESTION_IMAGE]=request.scheme + '://' + request.get_host() +"/media/"+ str(question_img_data.image_url) 
			response[keys.KEY_QUESTION]=temp_json
			response[keys.KEY_SUCCESS]=True
			response[keys.KEY_MESSAGE]="Success Finding QuestionData"
		except Exception as e:
			response[keys.KEY_SUCCESS]=False
			response[keys.KEY_MESSAGE]="Error Finding Question Image "+str(e)
	except Exception as e:
		response[keys.KEY_SUCCESS]=False
		response[keys.KEY_MESSAGE]="Error Finding Question "+str(e)
	print response
	return response

@csrf_exempt
def question_list(request):
	response_json={}
	if request.method == 'GET':
		try:
			access_token = request.GET.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json= jwt.decode(str(access_token),keys.KEY_ACCESS_TOKEN_ENCRYPTION,algorithms=['HS256'])
			mobile=str(json[keys.KEY_ACCESS_TOKEN])
			try:
				user_instance=UserData.objects.filter(mobile=mobile)
				if user_instance.exists():
					user_instance=UserData.objects.get(mobile=mobile)
					response_unsolved_question=unsolved_question(access_token)
					print "Return to Question_list_method"
					if response_unsolved_question[keys.KEY_SUCCESS]:
						next_question_no=response_unsolved_question[keys.KEY_NEXT_QUESTION]
						print str(next_question_no)
						response_question_data=question_data(request,next_question_no)
						if response_question_data[keys.KEY_SUCCESS]:
							response_json[keys.KEY_NEXT_QUESTION]=response_question_data[keys.KEY_QUESTION]
							solved_question_list=[]
							question_set=QuestionData.objects.all()
							question_set.order_by('question_no')
							question_set=question_set[:next_question_no-1]
							print "question_set"
							print question_set
							if question_set.count() > 0:
								for x in question_set:
									response_question_data=question_data(request,x.question_no)
									temp_question_data=response_question_data[keys.KEY_QUESTION]
									if response_question_data[keys.KEY_SUCCESS]:
										solved_question_list.append(temp_question_data)
							
							print "solved_question_list"	
							print solved_question_list
							response_json[keys.KEY_SOLVED_QUESTION_LIST]=solved_question_list
							response_json[keys.KEY_SUCCESS]=True
							response_json[keys.KEY_MESSAGE]="Success"
							
						else:
							response_json[keys.KEY_SUCCESS]=False
							response_json[keys.KEY_MESSAGE]="Error "+str(response_question_data[keys.KEY_MESSAGE])  
					else:
						if response_unsolved_question[keys.KEY_MESSAGE] == "All Questions Solved":
							solved_question_list=[]
							question_set=QuestionData.objects.all()
							question_set.order_by('question_no')
							print "question_set"
							print question_set
							if question_set.count() > 0:
								for x in question_set:
									response_question_data=question_data(request,x.question_no)
									temp_question_data=response_question_data[keys.KEY_QUESTION]
									if response_question_data[keys.KEY_SUCCESS]:
										solved_question_list.append(temp_question_data)
							
							print "solved_question_list"	
							print solved_question_list
							response_json[keys.KEY_SOLVED_QUESTION_LIST]=solved_question_list
							response_json[keys.KEY_SUCCESS]=True
							response_json[keys.KEY_MESSAGE]="All Questions Solved"
						else :
							response_json[keys.KEY_SUCCESS]=False
							response_json[keys.KEY_MESSAGE]="Error "+str(response_unsolved_question[keys.KEY_MESSAGE])  
				else:	
					response_json[keys.KEY_SUCCESS]=False
					response_json[keys.KEY_MESSAGE]="Invalid User"
			except Exception as e:
				print str(e)
				response_json[keys.KEY_SUCCESS]=False
				response_json[keys.KEY_MESSAGE]="Error finding UserInstance "+str(e)
		except Exception as e:
			print str(e)
			response_json[keys.KEY_SUCCESS]=False
			response_json[keys.KEY_MESSAGE]="Decoding Error "+str(e)

	elif request.method == 'POST':
		try:
			access_token = request.POST.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json= jwt.decode(str(access_token),keys.KEY_ACCESS_TOKEN_ENCRYPTION,algorithms=['HS256'])
			mobile=str(json[keys.KEY_ACCESS_TOKEN])
			try:
				user_instance=UserData.objects.filter(mobile=mobile)
				if user_instance.exists():
					user_instance=UserData.objects.get(mobile=mobile)
					answer = request.POST.get(keys.KEY_QUESTION_ANSWER)
					question_no = request.POST.get(keys.KEY_QUESTION_NO)
					try:
						question_datas=QuestionData.objects.get(question_no=question_no)
						stored_answer=question_datas.answer.replace(" ","")
						answer=answer.replace(" ","")
						if answer == stored_answer:
							try:
								user_question_data=UserQuestionData.objects.create(
																					user=user_instance,
																					question=question_datas,
																					answered=True,
																					)	
								setattr(user_instance,'last_question_answered', question_no)
								setattr(user_instance,'last_question_timestamp',user_question_data.timestamp)
								user_instance.save();
								print "Answer correct "+str(user_instance.last_question_answered)
								response_json[keys.KEY_SUCCESS]=True
								response_json[keys.KEY_MESSAGE]="Right Answer"
							except Exception as e:
								print str(e)
								response_json[keys.KEY_SUCCESS]=False
								response_json[keys.KEY_MESSAGE]="Error "+str(e)
								
						else :
							response_json[keys.KEY_SUCCESS]=False
							response_json[keys.KEY_MESSAGE]="Wrong Answer"
					except Exception as e:
						response_json[keys.KEY_SUCCESS]=False
						response_json[keys.KEY_MESSAGE]="Error "+str(e)
			except Exception as e:
				response_json[keys.KEY_SUCCESS]=False
				response_json[keys.KEY_MESSAGE]="Error "+str(e)

		except Exception as e:
				response_json[keys.KEY_SUCCESS]=False
				response_json[keys.KEY_MESSAGE]="Error "+str(e)
	print response_json
	return JsonResponse(response_json)

@csrf_exempt
def story(request):
	response={}
	if request.method == 'GET':
		try:
			access_token = request.GET.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json= jwt.decode(str(access_token),keys.KEY_ACCESS_TOKEN_ENCRYPTION,algorithms=['HS256'])
			mobile=str(json[keys.KEY_ACCESS_TOKEN])
			print mobile
			try:
				user_instance= UserData.objects.filter(mobile=mobile)
				if user_instance.exists():
					story=StoryData.objects.all()
					for o in story[:1]:
						response[keys.KEY_STORY]=o.content
						response[keys.KEY_STORY_IMAGE]=request.scheme + '://' + request.get_host() +"/media/"+ str(o.image)
					response[keys.KEY_SUCCESS]=True
					response[keys.KEY_MESSAGE]="Success"
				else :
					response[keys.KEY_SUCCESS]=False
					response[keys.KEY_MESSAGE]="Invalid User"
			except Exception as e:
				response[keys.KEY_SUCCESS]=False
				response[keys.KEY_MESSAGE]="Error "+str(e)
		except Exception as e:
			response[keys.KEY_SUCCESS]=False
			response[keys.KEY_MESSAGE]="Decoding Error "+str(e)
	print response
	return JsonResponse(response)

@csrf_exempt
def bonus(request):
	response={}
	if request.method == 'GET':
		try:
			access_token = request.GET.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json= jwt.decode(str(access_token),keys.KEY_ACCESS_TOKEN_ENCRYPTION,algorithms=['HS256'])
			mobile=str(json[keys.KEY_ACCESS_TOKEN])
			print mobile
			try:
				user_instance= UserData.objects.filter(mobile=mobile)
				if user_instance.exists():
					user_instance=UserData.objects.get(mobile=mobile)
					question = BonusQuestionData.objects.get(question_no=1)
					try:
						user_bonus_question_data=UserBonusQuestionData.objects.get(question=question,user=user_instance)
					except Exception as e:
						print str(e)
						user_bonus_question_data=UserBonusQuestionData.objects.create(
																					user=user_instance,
																					question=question,
																					answered=False
													)
					print str(user_bonus_question_data.answered)

					if user_bonus_question_data.answered:
						response[keys.KEY_ANSWERED]=True
					else:
						response[keys.KEY_ANSWERED]=False		
					temp_json={}
					temp_json[keys.KEY_QUESTION_NAME]=question.name
					temp_json[keys.KEY_QUESTION_NO]=question.question_no
					temp_json[keys.KEY_QUESTION_CONTENT]=question.content
					temp_json[keys.KEY_QUESTION_IMAGE]=request.scheme + '://' + request.get_host() +"/media/"+ str(question.image_url) 
					
					response[keys.KEY_QUESTION]=temp_json
					response[keys.KEY_SUCCESS]=True
					response[keys.KEY_MESSAGE]="Success"
				else:
					response[keys.KEY_SUCCESS]=False
					response[keys.KEY_MESSAGE]="Invalid User"					
			except Exception as e:
				response[keys.KEY_SUCCESS]=False
				response[keys.KEY_MESSAGE]="Error Finding User"
		except Exception as e:
			response[keys.KEY_SUCCESS]=False
			response[keys.KEY_MESSAGE]="Decoding Error "+str(e)

	elif request.method == 'POST':
		try:
			access_token = request.POST.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json= jwt.decode(str(access_token),keys.KEY_ACCESS_TOKEN_ENCRYPTION,algorithms=['HS256'])
			mobile=str(json[keys.KEY_ACCESS_TOKEN])
			print mobile
			try:
				user_instance= UserData.objects.filter(mobile=mobile)
				answer=request.POST.get(keys.KEY_QUESTION_ANSWER)
				if user_instance.exists():
					user_instance=UserData.objects.get(mobile=mobile)
					question = BonusQuestionData.objects.get(question_no=1)
					stored_answer=question.answer.replace(" ","")
					answer=answer.replace(" ","")
					if answer==stored_answer:
						user_bonus_question_data=UserBonusQuestionData.objects.get(question=question,user=user_instance)
						setattr(user_bonus_question_data,'answered',True)
						user_bonus_question_data.save();
						response[keys.KEY_SUCCESS]=True
						response[keys.KEY_MESSAGE]="Correct Answer"	
					else :
						response[keys.KEY_SUCCESS]=False
						response[keys.KEY_MESSAGE]="Wrong Answer"
				else:
					response[keys.KEY_SUCCESS]=False
					response[keys.KEY_MESSAGE]="Invalid User"					
			except Exception as e:
				response[keys.KEY_SUCCESS]=False
				response[keys.KEY_MESSAGE]="Error Finding User "+ str(e) 

		except Exception as e:
			response[keys.KEY_SUCCESS]=False
			response[keys.KEY_MESSAGE]="Decoding Error "+str(e)

	print response
	return JsonResponse(response)

@csrf_exempt
def hints(request):
	response={}
	if request.method == 'GET':
		try:
			access_token = request.GET.get(keys.KEY_ACCESS_TOKEN)
			print access_token
			json= jwt.decode(str(access_token),keys.KEY_ACCESS_TOKEN_ENCRYPTION,algorithms=['HS256'])
			mobile=str(json[keys.KEY_ACCESS_TOKEN])
			print mobile
			try:
				user_instance= UserData.objects.filter(mobile=mobile)
				answer=request.GET.get(keys.KEY_QUESTION_ANSWER)

				if user_instance.exists():
					hints_list=[]
					for o in QuestionHints.objects.all():
						temp_json={}
						temp_json[keys.KEY_QUESTION_NAME]=o.question.name
						temp_json[keys.KEY_QUESTION_NO]=o.question.question_no
						temp_json[keys.KEY_QUESTION_HINTS]=o.hint
						question_img_data = QuestionImageData.objects.get(question=o.question)
						temp_json[keys.KEY_QUESTION_IMAGE]=request.scheme + '://' + request.get_host() +"/media/"+ str(question_img_data.image_url) 
						hints_list.append(temp_json)
					response[keys.KEY_HINT_LIST]=hints_list
					response[keys.KEY_SUCCESS]=True
					response[keys.KEY_MESSAGE]="Success"
				else:
					response[keys.KEY_SUCCESS]=False
					response[keys.KEY_MESSAGE]="Invalid User"	
			except Exception as e:
				response[keys.KEY_SUCCESS]=False
				response[keys.KEY_MESSAGE]="Error Finding User"
		except Exception as e:
			response[keys.KEY_SUCCESS]=False
			response[keys.KEY_MESSAGE]="Decoding Error "+str(e)
	print response
	return JsonResponse(response)