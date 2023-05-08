from django.shortcuts import render, redirect

from .models import questions

#A03:2021 – Injection line 6-10
def find_topic(tid):
	for q in questions:
		if q['id'] == tid:
			return q
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


#Flaw 1: A01:2021 – Broken Access Control from line 53 to 59
def finishView(request):
	try:
		request.session['passed'] = 0
		return render(request, 'pages/finish.html')
	except:
		return redirect('/cheater/')
	#return render(request, 'pages/finish.html')


def cheaterView(request):
	return render(request, 'pages/cheater.html')


def thanksView(request):
	# Like we were going to pay anyone
	return render(request, 'pages/thanks.html')



def topicView(request, tid):
	request.session['passed'] = 0
	request.session['topic'] = tid
	print("SESSION TOPIC SET TO: ", tid)
	topic = find_topic(tid)
	return render(request, 'pages/topic.html', {'topic' : topic})


def topicsView(request):
	return render(request, 'pages/topics.html', {'questions' : questions})
