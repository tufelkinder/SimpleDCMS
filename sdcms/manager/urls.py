from django.conf.urls import patterns, include, url
from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('manager.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^go/(?P<page_name>[-\w]+)/', 'go'),
    url(r'^gallery/(?P<gal_id>\w+)/', 'gallery'),
    url(r'^gallery/', 'gallery'),
    url(r'^blog/(?P<blog_id>\w+)/', 'blog'),
    url(r'^blog/', 'blog'),
    url(r'^contact/', 'contact'),
    url(r'^g_path/(?P<g_id>\d+)/','g_path'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)
