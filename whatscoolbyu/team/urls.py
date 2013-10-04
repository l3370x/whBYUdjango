from django.conf.urls import *
from team.views import get_update_form, do_update2

urlpatterns = patterns('team.views',
			url(r'^create/$', 'create'),
			url(r'^home/$', 'teamDetails'),
			url(r'^delete/$', 'teamDelete'),
			url(r'^deleteReal/$', 'teamDeleteReal'),
			url(r'^all/$', 'allTeams'),
			url(r'^join/$', 'joinTeamRequest'),
			url(r'^update/$', 'update'),
			url(r'^updateProfile/$', 'editSettings'),
			url(r'^myProfile/$', 'myProfile'),
			url(r'^get_update_form$', get_update_form, name="get_update_form"),
			url(r'^do_update$', do_update2, name="do_update"),
			url(r'^leave/$', 'leave'),
			url(r'^leaveReal/$', 'leaveReal'),
			url(r'^allowJoin/$', 'allowJoinTeamRequest'),
			url('^details/(?P<team>[\w|\W]+)$', 'showTeam'),
			url(r'^(?P<username>\w+)$', 'userDetails'),
			)
