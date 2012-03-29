from django.contrib import admin
from sdcms.manager.models import *

    
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('slug','title','page','link','order')
    list_editable = ('title','order',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name','html',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('slug','title','template','show_in_navigation',)

    class Media:
        css = {
            'all': ('/media/css/page.css',),
        }
        js = ('/media/js/ckeditor/ckeditor.js','/media/js/page.js',)


class ElementAdmin(admin.ModelAdmin):
    list_display = ('name','description',)


class GraphicAdmin(admin.ModelAdmin):
    list_display = ('name','caption','image',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','date','content')
    search_fields = ('title','date','content')

#class GalleryAdmin(admin.ModelAdmin):
#    list_display = ('name','image',)


admin.site.register(NavigationItem,NavigationItemAdmin)
admin.site.register(Template,TemplateAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Element,ElementAdmin)
admin.site.register(Graphic,GraphicAdmin)
admin.site.register(Gallery)
admin.site.register(Article,ArticleAdmin)
