from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sdcms.manager.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^go/(?P<page_name>[-\w]+)/', 'go'),
    url(r'^gallery/(?P<gal_id>\w+)/', 'gallery'),
    url(r'^gallery/', 'gallery'),
    url(r'^blog/(?P<blog_id>\w+)/', 'blog'),
    url(r'^blog/', 'blog'),
    url(r'^contact/', 'contact'),
    url(r'^g_path/(?P<g_id>\d+)/','g_path'),

# this entry should be last
    url(r'^(?P<page_name>[-\w]+)$', 'go', name='go'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
