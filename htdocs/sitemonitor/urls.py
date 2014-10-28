from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from django.views.generic import TemplateView
from .views import WebSiteCreate

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #base template include
    url(r'^$', 'sitemonitor.views.home', name='home'),
    url(r'^$', WebSiteCreate.as_view(template_name='base.html')),

    url(r'^website/add/$', WebSiteCreate.as_view(), name='website_add'),
    url(r'^sites', 'sitemonitor.views.sites', name='sites'),
    url(r'^site/(?P<id>\w+)/$', 'sitemonitor.views.site', name='site'),
    url(r'^folder/(?P<id>\w+)/$', 'sitemonitor.views.folder', name='folder'),
    url(r'^file/(?P<id>\w+)/$', 'sitemonitor.views.file', name='file'),
    url(r'^file_approve/(?P<id>\w+)/$', 'sitemonitor.views.approve_change', name='approve_change'),


    #run scripts
    url(r'^directory_structure/', 'sitemonitor.views.directory_structure', name='directory_structure'),
    url(r'^check_for_changes/', 'sitemonitor.views.check_for_changes', name='check_for_changes'),

    #docs
    url(r'^contact', 'sitemonitor.views.contact', name='contact'),
    url(r'^faq', 'sitemonitor.views.faq', name='faq'),
    url(r'^documentation', 'sitemonitor.views.documentation', name='documentation'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #REST Framework
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #auth
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
