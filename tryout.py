#!/usr/bin/python
import sys
import os
from os import  listdir
from os.path import dirname
sys.path.insert(0, dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'emlprime.settings'

