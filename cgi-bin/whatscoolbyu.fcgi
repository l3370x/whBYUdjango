#!/usr/bin/python
import sys, os

basepath = '/homepages/19/d429491612/htdocs/byu'

sys.path.insert(0, basepath + '/.local/lib')
sys.path.insert(0, basepath + '/whatscoolbyu')

os.environ['DJANGO_SETTINGS_MODULE'] = 'whatscoolbyu.settings'



from django.core.servers.fastcgi import runfastcgi
runfastcgi(method='threaded', daemonize='false')
