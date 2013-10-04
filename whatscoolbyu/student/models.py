from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from django.views.generic.edit import UpdateView


class Student(models.Model):
	def __unicode__(self):
		return self.user.username
	def name(self):
		return self.user.username
	user = models.ForeignKey(User, editable=False)
	twitchName = models.CharField(max_length=50, blank=True)
	hideTwitch = models.BooleanField(default=False)
	hideSkype = models.BooleanField(default=False)
	hideEmail = models.BooleanField(default=False)
	skypeName = models.CharField(max_length=50, blank=True)
	myTeam = models.ForeignKey('Team',editable=False, blank=True, null=True,on_delete=models.SET_NULL)
	email = models.EmailField(blank=True)
	

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student

class StudentUpdate(UpdateView):
    model = Student
    fields = ['twitchName','hideTwitch','skypeName','hideSkype','email','hideEmail']
    template_name_suffix = '_update_form'

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)

class CreateUserForm(forms.Form):
	username = forms.CharField(max_length=100, label="Username")
	twitchName = forms.CharField(max_length=50,required=False, label="Twitch username")
	hideTwitch = forms.BooleanField(required=False, label="Hide twitch username?")
	skypeName = forms.CharField(max_length=50,required=False,label="Skype username")
	hideSkype = forms.BooleanField(required=False, help_text="Hide your skype username?", label="Hide skype username?")
	email = forms.EmailField(max_length=100,label="E-mail")
	hideEmail = forms.BooleanField(required=False, label="Hide e-mail address?")
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
	confirm = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
	
class EditUserForm(forms.Form):
	twitchName = forms.CharField(max_length=50,required=False, label="Twitch username")
	hideTwitch = forms.BooleanField(required=False, label="Hide twitch username?")
	skypeName = forms.CharField(max_length=50,required=False,label="Skype username")
	hideSkype = forms.BooleanField(required=False, help_text="Hide your skype username?", label="Hide skype username?")
	email = forms.EmailField(required=False,max_length=100,label="E-mail")
	hideEmail = forms.BooleanField(required=False, label="Hide e-mail address?")
	

class StudentChangePasswordForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(render_value=True), max_length=100)

class Team(models.Model):
	def __unicode__(self):
		return self.name
	def name(self):
		return self.name
	teamLeader = models.ForeignKey(Student, editable=False)
	name = models.CharField(max_length=50)
	captain = models.CharField(max_length=50,blank = True)
	helm = models.CharField(max_length=50,blank = True)
	weapons = models.CharField(max_length=50,blank = True)
	science = models.CharField(max_length=50,blank = True)
	engineering = models.CharField(max_length=50,blank = True)
	comms = models.CharField(max_length=50,blank = True)

class TeamForm(forms.ModelForm):
	class Meta:
		model = Team
		
class HelpForm(forms.Form):
	replyEmail=forms.EmailField(label="E-Mail for dev to reply to")
	subject=forms.CharField(label="Subject")
	question=forms.CharField(widget=forms.Textarea,label="Message")

class CreateTeamForm(forms.Form):
   teamName = forms.CharField(max_length=50,label="Team Name")
