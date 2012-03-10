from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sdcms.manager.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^go/(?P<page_name>\w+)/', 'go'),
    url(r'^gallery/(?P<gal_id>\w+)/', 'gallery'),
    url(r'^gallery/', 'gallery'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
