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
from request.models import *
from student.models import *
from news.models import *

@login_required
def leave(request):
	user = User.objects.get(username=request.user)
	stud = Student.objects.get(user=user)
	if stud.myTeam.teamLeader == stud:
		return render(request,'team/leaderLeave.html',{})
	return render(request,'team/confirmLeave.html',{})

@login_required
def leaveReal(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.user)
		stud = Student.objects.get(user=user)
		team = stud.myTeam
		if(team.captain == user.username):
			team.captain = ""
		if(team.helm == user.username):
			team.helm = ""
		if(team.weapons == user.username):
			team.weapons = ""
		if(team.science == user.username):
			team.science = ""
		if(team.engineering == user.username):
			team.engineering = ""
		if(team.comms == user.username):
			team.comms = ""
		team.save()
		stud.myTeam = None
		stud.save()
	return allTeams(request)

@login_required
def update(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.user)
		stud = Student.objects.get(user=user)
		team = Team.objects.get(teamLeader=stud)
		if team.teamLeader != stud:
			return teamDetails(request)
		if request.POST['position'] == 'captain':
			team.captain = request.POST['drop']
		if request.POST['position'] == 'helm':
			team.helm = request.POST['drop']
		if request.POST['position'] == 'weapons':
			team.weapons = request.POST['drop']
		if request.POST['position'] == 'science':
			team.science = request.POST['drop']
		if request.POST['position'] == 'engineering':
			team.engineering = request.POST['drop']
		if request.POST['position'] == 'comms':
			team.comms = request.POST['drop']
		team.save()
		return teamDetails(request)
	return teamDetails(request)
	
@login_required
def allowJoinTeamRequest(request):
	if request.method == 'POST':
		team = Team.objects.get(id=request.POST['team'])
		user = User.objects.get(id=request.POST['user'])
		stud = Student.objects.get(user=user)
		if Student.objects.get(user=request.user.id).myTeam != team:
			return allTeams(request)
		d = {}
		d['team']=team
		d['stud']=stud
		stud.myTeam = team
		stud.save()
		reqs = Request.objects.filter(fk_student=stud)
		for r in reqs:
			r.delete()
		return render(request,'team/requestAccepted.html',d)
	if request.method == 'GET':
		return allTeams(request)

@login_required
def teamDetails(request):
	stud = Student.objects.get(user=request.user.id)
	noTeam = stud.myTeam is None
	if noTeam:
		stud.myTeam = None
		return render(request,'team/myNoTeam.html',{})
	team = stud.myTeam
	teamLeader = stud == team.teamLeader
	if teamLeader:
		requests = Request.objects.filter(fk_team=team)
		myRequests = []
		for r in requests:
			toAdd = Student.objects.filter(id=r.fk_student.id)
			for rr in toAdd:
				myRequests.append(rr)
		teamMembers = Student.objects.filter(myTeam=team)
		return render(request,'team/home.html',{'myTeam':team,'teamLeader':teamLeader,'requests':myRequests,'teamMembers':teamMembers})
	teamMembers = Student.objects.filter(myTeam=team)
	return render(request,'team/home.html',{'myTeam':team,'teamLeader':teamLeader,'teamMembers':teamMembers})

def showTeam(request,team="00000000101"):
	try:
		theTeam = Team.objects.get(name=team)
		try:
			user = User.objects.get(id=request.user.id)
			stud = Student.objects.get(user=user)
			if stud.myTeam == theTeam:
				return teamDetails(request)
		except User.DoesNotExist:
			pass
		except Student.DoesNotExist:
			pass
		teamMembers = Student.objects.filter(myTeam=theTeam)
		return render(request,'team/home.html',{'myTeam':theTeam,'teamMembers':teamMembers})
	except Team.DoesNotExist:
		return render(request,'team/noTeam.html',{'noTeam':team})
	

@login_required
def teamDelete(request):
	stud = Student.objects.get(user=request.user.id)
	noTeam = stud.myTeam is None
	return render(request,'team/confirmDelete.html',{'noTeam':noTeam})

@login_required
def teamDeleteReal(request):
	stud = Student.objects.get(user=request.user.id)
	noTeam = stud.myTeam is None
	if noTeam:
		return render(request,'team/deleted.html',{})
	team = stud.myTeam
	if team.teamLeader == stud:
		team.delete()
		noTeam = True
		return render(request,'team/deleted.html',{'noTeam':noTeam})
	return teamDetails(request)

def allTeams(request):
	d = {}
	d['teams']=Team.objects.all()
	try:
		stud = Student.objects.get(user=request.user.id)
	except Student.DoesNotExist:
		#NOT LOGGED IN
		d['loggedIn']=False
		return render(request,'team/all.html',d)
	noTeam = stud.myTeam is None
	if noTeam:
		d['loggedIn']=True
		d['noTeam']=True
		d['teamLeader']=False
		d['me']=stud
		return render(request,'team/all.html',d)
	d['loggedIn']=True
	d['noTeam']=False
	d['teamLeader']=stud == stud.myTeam.teamLeader
	return render(request,'team/all.html',d)

@login_required
def joinTeamRequest(request):
	if request.method == 'POST':
		try:
			team = Team.objects.get(id=request.POST['team'])
		except Team.DoesNotExist:
			return render(request,'team/missing.html')
		user = User.objects.get(id=request.POST['user'])
		stud = Student.objects.get(user=user)
		d = {}
		d['team']=team
		d['stud']=stud
		check = Request.objects.filter(fk_team=team,fk_student=stud)
		if not check:
			newR = Request.objects.create(fk_team=team,fk_student=stud)
			return render(request,'team/requestSubmit.html',d)
		return render(request,'team/alreadyRequested.html',d)
	if request.method == 'GET':
		return allTeams(request)

@login_required
def myProfile(request):
	try:
		user = User.objects.get(id=request.user.id)
		stud = Student.objects.get(user=user)
	except User.DoesNotExist:
		return render(request,'user/noone.html',{'fakename':"unknown"})
	except Student.DoesNotExist:
		return render(request,'user/noone.html',{'fakename':"unknown"})
	return userDetails(request,user.username)

@login_required
def userDetails(request,username="noone"):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return render(request,'user/noone.html',{'fakename':username})
	stud = Student.objects.get(user=user)
	myself = False
	if request.user.id==user.id:
		myself = True
	return render(request,'user/detail.html',{'stud':stud,'myself':myself})
	
	
from django.utils import simplejson as json
from django.http import HttpResponse

def do_update2(request):
	resp = {}
	what = request.GET['what']
	user = User.objects.get(id=request.user.id)
	stud = Student.objects.get(user=user)
	if what=='twitch':
		stud.twitchName = request.GET['newValue1']
		if(request.GET['newValue2'] == 'true'):
			stud.hideTwitch = True
		else:
			stud.hideTwitch = False
		stud.save()
	if what=='skype':
		stud.skypeName = request.GET['newValue1']
		if(request.GET['newValue2'] == 'true'):
			stud.hideSkype = True
		else:
			stud.hideSkype = False
		stud.save()
	if what=='email':
		stud.email = request.GET['newValue1']
		if(request.GET['newValue2'] == 'true'):
			stud.hideEmail = True
		else:
			stud.hideEmail = False
		stud.save()
	return HttpResponse(json.dumps(resp), content_type="application/json")

def get_update_form(request):
	resp = {}
	what = request.GET['what']
	user = User.objects.get(id=request.user.id)
	stud = Student.objects.get(user=user)
	if what == 'twitch':
		formToAdd='<input id="in1" type="hidden" name="what" value="twitch">'\
							'<p>Twitch Name: <input id="in2" type="input" name="newValue1" value="'+stud.twitchName+'"></p>'\
							'<p>Hide Twitch Name? <input id="in3" type="checkbox" name="newValue2" value="'+str(stud.hideTwitch)+'"'
		if stud.hideTwitch:
			formToAdd += "checked"
		formToAdd += '></p><p><input type="submit" value="Update Twitch" onClick="doUpdate()"></p>'
		resp['formToAdd']=formToAdd
	if what == 'skype':
		formToAdd='<input id="in1" type="hidden" name="what" value="skype">'\
							'<p>Skype Name: <input id="in2" type="input" name="newValue1" value="'+stud.skypeName+'"></p>'\
							'<p>Hide Skype Name? <input id="in3" type="checkbox" name="newValue2" value="'+str(stud.hideSkype)+'"'
		if stud.hideSkype:
			formToAdd += "checked"
		formToAdd += '></p><p><input type="submit" value="Update Skype" onClick="doUpdate()"></p>'
		resp['formToAdd']=formToAdd
	if what == 'email':
		formToAdd='<input id="in1" type="hidden" name="what" value="email">'\
							'<p>E-Mail: <input id="in2" type="input" name="newValue1" value="'+stud.email+'"></p>'\
							'<p>Hide E-mail? <input id="in3" type="checkbox" name="newValue2" value="'+str(stud.hideEmail)+'"'
		if stud.hideEmail:
			formToAdd += "checked"
		formToAdd += '></p><p><input type="submit" value="Update Email" onClick="doUpdate()"></p>'
		resp['formToAdd']=formToAdd
	return HttpResponse(json.dumps(resp), content_type="application/json")

def updateTwitch(request,user,stud):
	return render(request,"debug.html")

@login_required
def editSettings(request):
	d = {}
	user = User.objects.get(id=request.user.id)
	stud = Student.objects.get(user=user)
	what = request.GET['what']
	if what == "twitch":
		return updateTwitch(request,user,stud)
	d['user']=user
	d['stud']=stud
	d['what']=what
	
	return render(request,"debug.html",d)
	
	
@login_required
def create(request):
	user = User.objects.get(id=request.user.id)
	d = {}
	if request.method == 'GET':
		form = CreateTeamForm()
		stud = Student.objects.get(user=user)
		if stud.myTeam != None:
			return render(request,'team/alreadyHaveTeam.html',{'myTeam':stud.myTeam})
		return render_to_response('team/create.html',{'form':form},context_instance = RequestContext(request))
	if request.method == 'POST':
		form = CreateTeamForm(request.POST)
		if not form.is_valid():
			return render_to_response('team/create.html',{'form':form},context_instance = RequestContext(request))
		try:
			u = Team.objects.get(name = request.POST['teamName'])
			d['error'] = 'Team name already taken'
			d['form'] = form
			return render_to_response('team/create.html', d, context_instance = RequestContext(request))
		except Team.DoesNotExist:
			pass
		currentStud = Student.objects.get(user=request.user.id)
		newTeam = Team.objects.create(teamLeader=currentStud,name=request.POST['teamName'],captain="",helm="",weapons="",science="",engineering='',comms='')
		currentStud.myTeam = newTeam
		currentStud.save()
		d['myTeam']=newTeam
		newNews = News.objects.create(user=user,title="New Team Created",
									message="Welcome "+newTeam.name+" to the GiantWaffle Artemis SBS Website.")
		return render(request,'team/createSuccess.html',d)
