from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WebSiteForm
from tables import FolderTable, FileTable
from .models import File, Folder
import datetime
import os
import subprocess
from django.db import connection

from .models import WebSite, Folder, File

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')


class WebSiteCreate(CreateView):
    """
    Create a new site based on submitted form
    """

    form_class = WebSiteForm
    model = WebSite

    def get_object(self, queryset=None):
        obj = WebSite.objects.get(pk=id)
        return obj

    def form_invalid(self, form):
        #messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        form.save(commit=True)

        return HttpResponseRedirect('/sites')

def sites(request):
    latest_site_list = WebSite.objects.order_by('-create_date')[:5]
    context = {'latest_site_list': latest_site_list}
    return render(request, 'sitemonitor/index.html', context)

def site(request, id):
    sites = WebSite.objects.get(pk=id)
    folders = Folder.objects.filter(website__id=id)
    table = FolderTable(folders)
    return render(request, 'sitemonitor/detail.html', {'sites': sites, 'table':table})

def folder(request, id):
    sites = WebSite.objects.get(folder__id=id)
    folders = Folder.objects.get(id=id)
    files = File.objects.filter(folder__id=id)
    table = FileTable(files)
    return render(request, 'sitemonitor/folder.html', {'sites':sites, 'folders': folders,'table':table})

def file(request,id):
    site = WebSite.objects.get(folder__file__id=id)
    folder = Folder.objects.get(file__id=id)
    file = File.objects.get(id=id)
    return render(request, 'sitemonitor/file.html', {'site':site, 'file': file, 'folder': folder})

def approve_change(request,id):
    if request.method == 'POST':

        file_save = File.objects.filter(pk=id).update(unverified_change=0)
        #check the folder for other unverified changes
        folder = File.objects.get(pk=id)
        check_folder = File.objects.filter(folder_id=folder.folder_id,unverified_change=1).count()
        #if there aren't any update folder
        if check_folder == 0:
            Folder.objects.filter(pk=folder.folder_id).update(unverified_change=0)

        redirect_url = '/file/' + id + '/'
    return redirect(redirect_url)

def filetree(request,folder_id):
    path=folder.folder_path
    # insert the path to the directory including the trailing '/'
    dirList=sorted(os.listdir(path))
    return render_to_response('directory_list/list.html', {'dirlist': dirList})

def foldertree(folder_path):
    path=folder_path
    # insert the path to the directory including the trailing '/'
    dirList=sorted(os.listdir(path))
    return render_to_response('sitemonitor/detail.html', {'dirlist': dirList})

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def documentation(request):
    return render(request, 'documentation.html')

#EXECUTE SCRIPTS
def directory_structure(request):
    process = subprocess.Popen(['python', 'manage.py', 'runscript directory_structure'])

    os.system("python manage.py runscript directory_structure")

    return render(request, 'directory_structure.html')

def check_for_changes(request):
    process = subprocess.Popen(['python', 'manage.py', 'runscript check_for_changes'])
    os.system("python manage.py runscript check_for_changes")
    return render(request, 'check_for_changes.html')


