from django.contrib import admin
from manager.models import *

    
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('slug','name','page','link','order')
    list_editable = ('name','order',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name','html',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('slug','title','template','show_in_navigation',)

    class Media:
        css = {
            'all': ('/media/css/page.css',),
        }
        js = ('/media/js/ckeditor/ckeditor.js','/media/js/page.js','/static/filebrowser/js/FB_CKEditor.js')


class ElementAdmin(admin.ModelAdmin):
    list_display = ('name','description',)


class GraphicAdmin(admin.ModelAdmin):
    list_display = ('name','caption','image','to_path',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','date','content','published')
    search_fields = ('title','date','content')
    list_editable = ('published',)

    class Media:
        css = {
            'all': ('/media/css/page.css',),
        }
        js = ('/media/js/ckeditor/ckeditor.js','/media/js/page.js','/static/filebrowser/js/FB_CKEditor.js')


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    exclude = ('thumb',)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name','image',)
    inlines = [PhotoInline,]


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','company','phone','email','date')
    search_fields = ('first_name','last_name','company','phone','email',)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name','pdf','to_path',)


admin.site.register(NavigationItem,NavigationItemAdmin)
admin.site.register(Template,TemplateAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Element,ElementAdmin)
admin.site.register(Graphic,GraphicAdmin)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(Photo)