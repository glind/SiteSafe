from django.db import models
from django.contrib import admin

class WebSite(models.Model):
    site_name = models.CharField(max_length=765, blank=True)
    site_url = models.TextField(blank=True)
    site_is_local = models.BooleanField(default=False)
    site_path = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.site_name

class WebSiteAdmin(admin.ModelAdmin):
    list_display = ('site_name','site_url','site_is_local','site_path')
    display = 'Web Sites'

class Folder(models.Model):
    folder_path = models.CharField(max_length=765, blank=True)
    folder_name = models.CharField(max_length=765, blank=True)
    num_files = models.CharField(max_length=765,blank=True)
    new_num_files = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    unverified_change = models.BooleanField(default=0)
    website = models.ForeignKey(WebSite)

    def __unicode__(self):
        return self.folder_name

class FolderAdmin(admin.ModelAdmin):
    list_display = ('folder_name','folder_path','num_files')
    display = 'Folders'


class File(models.Model):
    file_type = models.CharField(max_length=135, blank=True)
    file_path = models.CharField(max_length=765, blank=True)
    file_name = models.CharField(max_length=765, blank=True)
    file_hash = models.TextField(blank=True)
    file_hash_changed = models.TextField(blank=True)
    file_new = models.BooleanField(default=0)
    unverified_change = models.BooleanField(default=0)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    folder = models.ForeignKey(Folder)

    def __unicode__(self):
        return self.file_name

class FileAdmin(admin.ModelAdmin):
    list_display = ('file_type','file_path','file_name')
    display = 'Files'


class User(models.Model):
    user_name = models.CharField(unique=True, max_length=135, blank=True)
    email = models.CharField(max_length=765, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    list_display = ('user_name','email')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name','email')

admin.site.register(User,UserAdmin)
admin.site.register(File,FileAdmin)
admin.site.register(Folder,FolderAdmin)
admin.site.register(WebSite,WebSiteAdmin)


