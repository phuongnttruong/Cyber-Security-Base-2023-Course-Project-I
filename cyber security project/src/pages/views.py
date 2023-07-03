from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import questions
import sqlite3


#flaw 2: injection line 8-15
def find_topic(tid):
    connection = sqlite3.connect(Path(__file__).resolve().parent.parent / 'db.sqlite3')
    cursor = connection.cursor()
    query = "SELECT * FROM questions WHERE id = " + tid
    result = cursor.execute(query)  # Execute the query using a database connection
    connection.commit()
    connection.close()
    return result
#how to fix flaw 2: line 17-30
'''
def find_topic(tid):
    connection = sqlite3.connect(Path(__file__).resolve().parent.parent / 'db.sqlite3')
    cursor = connection.cursor()

    query = "SELECT * FROM questions WHERE id = ?"
    cursor.execute(query, (tid,))
    
    result = cursor.fetchall()
    
    connection.commit()
    connection.close()
    
    return result
'''

# flaw 3: line 34-41
def quizView(request, tid):
    print("CURRENTLY ON TOPIC: ", request.session['topic'])
    topic = find_topic(tid)

    user_input = request.GET.get('level')  # Get user input from the request
    request.session['level'] = int(user_input)  # Insecurely use user input without validation
    request.session['passed'] = 0
    return render(request, 'pages/question.html', {'topic': topic, 'question': topic['questions'][request.session['level']]})

# How to fix flaw 3: line 44-60
'''
def quizView(request, tid):
    print("CURRENTLY ON TOPIC: ", request.session['topic'])
    topic = find_topic(tid)

    user_input = request.GET.get('level')
    if user_input is not None and user_input.isdigit():
        level = int(user_input)
        if level >= 0 and level < len(topic['questions']):
            request.session['level'] = level
        else:
            request.session['level'] = 0
    else:
        request.session['level'] = 0

    request.session['passed'] = 0
    return render(request, 'pages/question.html', {'topic': topic, 'question': topic['questions'][request.session['level']]})
'''


def answerView(request, tid, aid):
	request.session['passed'] = 0
	print("CURRENTLY ON TOPIC: ", request.session['topic'])
	if request.session['topic'] != tid or request.session['level'] == -1 :
		return redirect('/cheater/')
		
	topic = find_topic(tid)

	level = request.session['level']
	print("currently at level: ", level)
	if topic['questions'][level]['correct'] == aid:
		level += 1
		request.session['level'] = level

		if level == len(topic['questions']):
			request.session['level'] = -1
			request.session['passed'] = 1
			print("level reset to: ", request.session['level'])
			return redirect('/finish/')

		return render(request, 'pages/question.html', {'topic' : topic, 'question' : topic['questions'][level]})
	else:
		return redirect('/incorrect/')


def incorrectView(request):
	request.session['level'] = -1
	return render(request, 'pages/incorrect.html')

#to fix flaw 5, we import csrf_protect to protect against cross-site request forgery
'''
from django.views.decorators.csrf import csrf_protect
@csrf_protect
'''

def finishView(request):
	try:
		request.session['passed'] = 0
		return render(request, 'pages/finish.html')
	except:
		return redirect('/cheater/')


def cheaterView(request):
	return render(request, 'pages/cheater.html')


def thanksView(request):
	# Like we were going to pay anyone
	return render(request, 'pages/thanks.html')


#flaw 1: line 74 to 81, the 'passed' session variable will always be set to 1, 
# regardless of the actual value of the 'passed' parameter. 
# This could potentially allow unauthorized access to certain resources or functionalities 
# that are intended to be restricted based on the value of 'passed'.
def topicView(request, tid):
    passed = request.GET.get('passed')  # Retrieve the 'passed' parameter from the request
    request.session['passed'] = 1  # Set 'passed' session variable to 1 unconditionally

    request.session['topic'] = tid
    print("SESSION TOPIC SET TO: ", tid)
    topic = find_topic(tid)
    return render(request, 'pages/topic.html', {'topic': topic})
#How to fix flaw 1, from line 89-99
'''
def topicView(request, tid):
    passed = request.GET.get('passed')  # Retrieve the 'passed' parameter from the request
    if passed == '1':
        request.session['passed'] = 1
    else:
        request.session['passed'] = 0

    request.session['topic'] = tid
    print("SESSION TOPIC SET TO: ", tid)
    topic = find_topic(tid)
    return render(request, 'pages/topic.html', {'topic': topic})
'''

def topicsView(request):
	return render(request, 'pages/topics.html', {'questions' : questions})
