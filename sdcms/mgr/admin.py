from __future__ import unicode_literals

from django.contrib import admin
from mgr.models import *

# Register your models here.

class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('slug','name','page','link','order')
    list_editable = ('name','order',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('slug','title','show_in_navigation',)

#    class Media:
#        css = {
#            'all': ('/media/css/page.css',),
#        }
#        js = ('/media/js/ckeditor/ckeditor.js','/media/js/page.js','/static/filebrowser/js/FB_CKEditor.js')


class SectionAdmin(admin.ModelAdmin):
    list_display = ('page','slug','title','show_in_navigation',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','date','content','published')
    search_fields = ('title','date','content')
    list_editable = ('published',)

#    class Media:
#        css = {
#            'all': ('/media/css/page.css',),
#        }
#        js = ('/media/js/ckeditor/ckeditor.js','/media/js/page.js','/static/filebrowser/js/FB_CKEditor.js')


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    exclude = ('thumb',)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name','image',)
    inlines = [PhotoInline,]


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','email','date')
    search_fields = ('first_name','last_name','phone','email',)


admin.site.register(NavigationItem,NavigationItemAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Photo)