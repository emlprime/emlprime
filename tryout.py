#!/usr/bin/python
import sys
import os
from os import  listdir
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'emlprime.settings'

from django.core.mail import mail_admins

message =  "%s\n%s\n%s" % ("eat", "more", "lemmings")
mail_admins('Project Request Submitted', message, fail_silently=False)
