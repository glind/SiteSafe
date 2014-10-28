#Get the full contents of each site by recursing through the parent directories and sub directoreis
#Check each file for differences to the original hash and check for new files in a folder
#Install module django-extensions is installed
#to execute :$ python manage.py runscript check_for_changes
from django.db import connection,transaction
cursor = connection.cursor()
from os.path import exists
from django.db import models
from sitemonitor.models import Folder, File, WebSite
import os
import sys
import mimetypes
import hashlib
from datetime import date

today = date.today()
today.strftime('%Y-%m-%d %hh:%mm')
today = str(today)
print today

def run():
	print "test"
