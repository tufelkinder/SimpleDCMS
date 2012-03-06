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
            "all": ('/media/css/editor.css'),
        }
        js = ('/media/js/jquery-min.js','/media/js/editor.js',)


class ElementAdmin(admin.ModelAdmin):
    list_display = ('name','description',)


class GraphicAdmin(admin.ModelAdmin):
    list_display = ('name','caption','image',)


admin.site.register(NavigationItem,NavigationItemAdmin)
admin.site.register(Template,TemplateAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Element,ElementAdmin)
admin.site.register(Graphic,GraphicAdmin)

