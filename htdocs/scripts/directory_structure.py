#Get the full contents of each site by recursing through the parent directories and sub directoreis
#Save each file hash and date to the database and store the contents of each folder
#Install module django-extensions is installed
#to execute :$ python manage.py runscript directory_structure
from django.db import connection,transaction
cursor = connection.cursor()
from os.path import exists
from django.db import models
from sitemonitor.models import Folder,File,WebSite
import os
import sys
import mimetypes
import hashlib
from datetime import date, datetime
from django.utils.timezone import make_aware
from django.utils import timezone


today_date = datetime.now()
today_date_tz = make_aware(today_date,timezone.get_default_timezone())
today = str(today_date)
print today

def run():
    print "Checking Directory Tree"

def getSiteContents(rootdir,site_id):
    for dirname, dirnames, filenames in os.walk(rootdir):
        #print "DIRNAME=" + dirname
        folder_path, folder_name = os.path.split(dirname)

        # print path to all subdirectories first.
        file_count = 0

        #save the folder info
        folder2 = Folder(folder_name=folder_name.strip(), folder_path=folder_path.strip(),create_date=today,num_files=file_count,website_id=site_id)
        folder2.save()
        folder_id = folder2.id

        # Get the filename for all files in the folder and generate attribute data.
        for filename in filenames:
            full_path =  os.path.join(dirname, filename)
            #check and save the file type
            type,encoding = mimetypes.guess_type(full_path)
            file_type = str(type)
            #generate an md5 hash for file
            file_for_hash = open(full_path,'rb')
            hash_value = md5_for_file(file_for_hash)
            #Pass file attributes to File object for saving then save
            file2 = File(file_name=filename.strip(), file_path=dirname.strip(),create_date=today,file_type=file_type,file_hash=hash_value,folder_id=folder_id)
            file2.save()
            file_id = file2.id
            file_count = file_count + 1

            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')

        #update folder with new file count
        get_folder = Folder.objects.get(id=folder_id)
        get_folder.num_files = file_count
        get_folder.save()


def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
try:
    #get all files and folders in a site
    site_list = WebSite.objects.all()
except Exception as e:
    print e

for site in site_list:
    print site.site_path
    print site.id
    #if the site
    if site.create_date <= today_date_tz:
        print "Cataloging " + site.site_name + " site"
        getSiteContents(site.site_path,site.id)


print "Alright, all done."
