from django.db import models
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your models here.


class NavigationItem(models.Model):
    slug = models.CharField("Short name",max_length=255,null=True,help_text="No spaces.")
    title = models.CharField(max_length=255,null=True,blank=True)
    page = models.ForeignKey('Page',null=True,blank=True)
    link = models.CharField(max_length=255,null=True,blank=True)
    order = models.IntegerField(null=True,blank=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.slug


class Template(models.Model):
    name = models.CharField(max_length=255,null=True)
    html = models.FileField(upload_to='templates',null=True,blank=True)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    slug = models.CharField("Short name",max_length=255,null=True,help_text="No spaces.")
    title = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    template = models.ForeignKey(Template,null=True,blank=True,help_text="Leave empty to use standard 'page.html' template.")
    header = models.ForeignKey('Graphic',null=True,blank=True,related_name="header_img")
    sidebar = models.ForeignKey('Graphic',null=True,blank=True,related_name="sidebar_img")
    show_in_navigation = models.BooleanField(default=False)

    def __unicode__(self):
        return self.slug


class Element(models.Model):
    name = models.CharField("Short name",max_length=255,null=True,help_text='Avoid spaces.')
    description = models.CharField(max_length=255,null=True,blank=True,help_text="Explain the purpose of this element.")
    content = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return self.name


class Graphic(models.Model):
    name = models.CharField("Short name",max_length=255,null=True,help_text="Avoid spaces.")
    caption = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='img',null=True,blank=True)
    thumb = models.ImageField(upload_to='img/thumb',null=True,blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        # We use PIL's Image object
        # Docs: http://www.pythonware.com/library/pil/handbook/image.htm
        # for additional comments: http://superjared.com/entry/django-quick-tips-2-image-thumbnails/
        # http://biohackers.net/wiki/Django1.0/Thumbnail
        if self.image and not self.thumb:
            THUMBNAIL_SIZE = (100,100)

            thmb = Image.open(self.image)

            if thmb.mode not in ('L', 'RGB'):
                thmb = thmb.convert('RGB')

            thmb.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            # Save the thumbnail
            temp_handle = StringIO()
            thmb.save(temp_handle, "JPEG")
            temp_handle.seek(0)

            # Save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                    temp_handle.read())
            self.thumb.save(suf.name, suf, save=False)

        super(Graphic, self).save()


    
class Gallery(models.Model):
    title = models.CharField(max_length=255,null=True)
    image = models.ForeignKey('Photo',null=True,blank=True)

    def __unicode__(self):
        return self.title


class Photo(models.Model):
    caption = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='img',null=True,blank=True)
    thumb = models.ImageField(upload_to='img/thumb',null=True,blank=True)

    def __unicode__(self):
        return self.caption

    def save(self):
        # We use PIL's Image object
        # Docs: http://www.pythonware.com/library/pil/handbook/image.htm
        # for additional comments: http://superjared.com/entry/django-quick-tips-2-image-thumbnails/
        # http://biohackers.net/wiki/Django1.0/Thumbnail
        if self.image and not self.thumb:
            THUMBNAIL_SIZE = (100,100)

            thmb = Image.open(self.image)

            if thmb.mode not in ('L', 'RGB'):
                thmb = thmb.convert('RGB')

            thmb.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            # Save the thumbnail
            temp_handle = StringIO()
            thmb.save(temp_handle, "JPEG")
            temp_handle.seek(0)

            # Save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                    temp_handle.read())
            self.thumb.save(suf.name, suf, save=False)

        super(Photo, self).save()


class Article(models.Model):
    title = models.CharField(max_length=255,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    content = models.TextField(null=True,blank=True)
    image = models.ForeignKey(Photo,null=True,blank=True)

    def save(self):
        if self.image and not self.thumb:
            THUMBNAIL_SIZE = (400,400)

            thmb = Image.open(self.image)

            if thmb.mode not in ('L', 'RGB'):
                thmb = thmb.convert('RGB')

            thmb.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            # Save the thumbnail
            temp_handle = StringIO()
            thmb.save(temp_handle, "JPEG")
            temp_handle.seek(0)

            # Save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                    temp_handle.read())
            self.thumb.save(suf.name, suf, save=False)

        super(Article, self).save()
