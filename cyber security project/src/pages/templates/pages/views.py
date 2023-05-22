from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import questions

#flaw 2: injection line 6
def find_topic(tid):
	query = "SELECT * FROM topics WHERE id = " + str(tid)
	with topicView.cursor() as cursor:
		cursor.execute(query)
		topic = cursor.fetchone()
	if topic:
		return topic
	return None


def quizView(request, tid):
	print("CURRENTLY ON TOPIC: ", request.session['topic'])
	topic = find_topic(tid)

	request.session['level'] = 0
	request.session['passed'] = 0
	return render(request, 'pages/question.html', {'topic' : topic, 'question' : topic['questions'][0]})



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


#flaw 1: line 74 to 84
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


def topicsView(request):
	return render(request, 'pages/topics.html', {'questions' : questions})
