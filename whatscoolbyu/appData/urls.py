from django.conf.urls import *


urlpatterns = patterns('student.views',
			url(r'^home/$', 'Home'),
			url(r'^$', 'Home'),
			)
