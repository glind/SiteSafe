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
from datetime import datetime

today = datetime.now()
today = str(today)
print today

def run():
    print "Checking Directory Tree"
def checkFiles(filenames,dirname,folder_id):
    #set local vars
    status = {'file_count':0,'unverified_change':0}
    # print path to all filenames.
    for filename in filenames:

        full_path =  os.path.join(dirname, filename)
        type,encoding = mimetypes.guess_type(full_path)
        file_type = str(type)
        file_for_hash = open(full_path,'rb')
        hash_value = md5_for_file(file_for_hash)
        #check for prior existence of File
        file_check = File.objects.get(file_name = filename, folder__id = folder_id)

        if not file_check:
            #It's a new file
            print "New File:" + filename + "\n"
            file2 = File(file_name=filename.strip(), file_path=dirname.strip(),create_date=today,file_type=file_type,file_hash=hash_value,unverified_change=True,folder_id=folder_id)
            file2.save()
            file_id = file2.id
            file2.folder.add(folder2)
            status['unverified_change'] = True
            print "New File detected: " + file2.file_name + "\n"
        #It's an old file
        else:
            #check the hash value
            if file_check.file_hash != hash_value:
                file_check.file_hash=hash_value
                file_check.edit_date=today
                file_check.unverified_change = True
                file_check.save()
                status['unverified_change'] = 1
                print "Change detected in: " + file_check.file_name + "\n"
            status['file_count'] = status['file_count'] + 1
    return status

def getSiteContents(rootdir,site_id):
    #set local vars
    file_status = {'file_count':0,'unverified_change':0}
    for dirname, dirnames, filenames in os.walk(rootdir):
        print "DIRNAME=" + dirname
        folder_path, folder_name = os.path.split(dirname)
        #check for prior existence of folder
        try:
            folder_check = Folder.objects.get(folder_name = folder_name,folder_path=folder_path)
            #old folder check the files and count
            if folder_check:
                file_status = checkFiles(filenames,dirname,folder_check.id)

                #if the file count is different update the count and modified date
                if (folder_check.num_files != file_status['file_count']) is False:
                    print folder_check.num_files + "!=" + str(file_status['file_count']) + "\n"
                    folder_check.num_files = file_status['file_count']
                    folder_check.edit_date = today
                    folder_check.unverified_change = 1
                    folder_check.save()
                else:
                    print folder_check.num_files + "=" + str(file_status['file_count']) + "\n"

                #if a change in a file in the folder was detected update edit date and unverified change
                if file_status['unverified_change'] == 1:
                    folder_check.edit_date = today
                    folder_check.unverified_change = 1
                    folder_check.save()

            else:
                #new folder save the folder info
                print "New Folder:" + folder_name.strip() + "\n"

                folder2 = Folder(folder_name=folder_name.strip(), folder_path=folder_path.strip(),create_date=today,num_files=file_status['file_count'],website_id=site_id)
                folder2.save()
                folder_id = folder2.id
                file_status = checkFiles(filenames,dirname,folder_id)
                folder2.num_files = file_status['file_count']
                folder_check.unverified_change = 1
                folder2.save()
        except Exception as e:
            print e

    #if a file changed then update the last edit date on folder otherwise it's a new folder
    if file_status['unverified_change'] == 1:
        folder_check.edit_date = today
        folder_check.new_num_files = file_status['file_count']
        folder_check.unverified_change = True
        folder_check.save()

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

#get all files and folders in a site
site_list = WebSite.objects.all()

for site in site_list:
    print site.site_path
    print site.id
    print "Checking " + site.site_name + " site"
    getSiteContents(site.site_path,site.id)


print "Alright, all done."
