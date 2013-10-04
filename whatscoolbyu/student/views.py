from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail

from student.models import *
from news.models import *
import pytz

def startPage(request):
	if request.user.is_authenticated():
		return Home(request)
	return login(request)

def Home(request):
	allNews = News.objects.all().order_by('-timestamp')[:8]
	try:
		stud = Student.objects.get(user=request.user.id)
		noTeam = stud.myTeam is None
		return render(request, 'home.html', {'allNews':allNews,'username':request.user.username,'noTeam':noTeam})
	except Student.DoesNotExist:
		pass
	return render(request,'home.html',{'allNews':allNews,'username':request.user.username})

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        tz = request.session.get('django_timezone')
        if tz:
            timezone.activate(tz)
        else:
            timezone.deactivate()

def Calendar(request):
	if request.method == 'POST':
		request.session['django_timezone'] = pytz.timezone(request.POST['timezone'])
	tz = request.session.get('django_timezone')
	if tz:
			timezone.activate(tz)
	tzout=str(tz).replace("/","%2F")
	try:
		stud = Student.objects.get(user=request.user.id)
		noTeam = stud.myTeam is None
		return render(request,'calendar.html',{'timezones': pytz.common_timezones,'tztext':tzout,'noTeam':False},)
	except Student.DoesNotExist:
		pass
	return render(request,'calendar.html',{'timezones': pytz.common_timezones,'tztext':tzout,'noTeam':True},)
	

def logout(request):
	django.contrib.auth.logout(request)
	return startPage(request)

def login(request):
	if request.method == 'GET':
		form = LoginForm()
		return render_to_response('auth/login.html', {'form':form},
								  context_instance = RequestContext(request))

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render_to_response('auth/login.html', {'form':form},
								  context_instance = RequestContext(request))

		user = authenticate(username = request.POST['username'],
							password = request.POST['password'])
		if user is None:
			return render_to_response('auth/login.html',
									  {'form':form,
									   'error': 'Invalid username or password'},
									  context_instance = RequestContext(request))
		django.contrib.auth.login(request, user)
		return student2Home(request, user)
	
def create(request):
	d = {}
	if request.method == 'GET':
		form = CreateUserForm()
		return render_to_response('student/create.html', {'form':form},
								  context_instance = RequestContext(request))

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if not form.is_valid():
			return render_to_response('student/create.html', {'form':form},
								  context_instance = RequestContext(request))

		try:
			u = User.objects.get(username = request.POST['username'])
			d['error'] = 'Username already taken'
			d['form'] = form
			return render_to_response('student/create.html', d, context_instance = RequestContext(request))
		except User.DoesNotExist:
			pass


		userO = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password']);
		userO.save
		person = Student.objects.create(user = userO, twitchName = request.POST['twitchName'],
											skypeName = request.POST['skypeName'],
											email = request.POST['email'])
		auth_user = authenticate(username=request.POST['username'],password=request.POST['password'])
		if auth_user is not None:
			django.contrib.auth.login(request, auth_user)
			return Home(request)
		d['error']="There was a server error creating your username, please try again."
		return render_to_response('student/create.html', d, context_instance = RequestContext(request))



def submitQuestion(request):
	d = {}
	if request.method == "GET":
		form = HelpForm()
		d['form']=form
		return render(request,'help.html',d)
	if request.method == "POST":
		form = HelpForm(request.POST)
		if not form.is_valid():
			return render(request,'help.html',d)
	send_mail(request.POST['subject'], request.POST['question'], request.POST['replyEmail'],
    ['l3370x@gmail.com'], fail_silently=False)
	return render(request,'helpThanks.html',d)

@login_required
def student2Home(request, studentUser):
	theStudent = Student.objects.get(user = studentUser.id)
	return redirect('/', {'theStudent':theStudent})
