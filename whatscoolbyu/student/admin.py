from student.models import Student,Team
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
  fieldsets = [
	('User Info', {'fields': ['user']}),
	('Twitch name', {'fields': ['twitchName']}),
	('Skype name', {'fields': ['skypeName']}),
	('email', {'fields': ['email']}),
	('myTeam', {'fields': ['myTeam']}),
  ]
  readonly_fields = ('user','myTeam',)

admin.site.register(Student, StudentAdmin)

class TeamAdmin(admin.ModelAdmin):
  fieldsets = [
	('Team Leader', {'fields': ['teamLeader']}),
	('Team Name', {'fields': ['name']}),
	('captain', {'fields': ['captain']}),
	('helm', {'fields': ['helm']}),
	('weapons', {'fields': ['weapons']}),
	('science', {'fields': ['science']}),
	('engineering', {'fields': ['engineering']}),
	('comms', {'fields': ['comms']}),
  ]
  readonly_fields = ('teamLeader',)

admin.site.register(Team, TeamAdmin)

