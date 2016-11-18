from __future__ import unicode_literals
import os
from StringIO import StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

# Create your models here.

class NavigationItem(models.Model):
    slug = models.CharField("Short name",max_length=255,null=True,help_text="No spaces.")
    name = models.CharField("Display name",max_length=255,null=True,blank=True)
    parent = models.ForeignKey('self',null=True,blank=True,help_text="Leaving this blank creates a new navigation option which may affect the layout of the site.")
    section = models.ForeignKey('Section',null=True,blank=True)
    page = models.ForeignKey('Page',null=True,blank=True)
    link = models.CharField(max_length=255,null=True,blank=True)
    order = models.IntegerField(null=True,blank=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.slug

    def children(self):
        return NavigationItem.objects.filter(parent=self)


class Page(models.Model):
    slug = models.CharField("Short name",max_length=255,null=True,help_text="No spaces.")
    title = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    show_in_navigation = models.BooleanField(default=False)

    def __unicode__(self):
        return self.slug

    def save(self):
        super(Page, self).save()
        if self.show_in_navigation:
            navitem, created = NavigationItem.objects.get_or_create(page=self)
            navitem.slug=self.slug
            navitem.name=self.title
            navitem.page=self
            navitem.save()
        else:
            navitems = NavigationItem.objects.filter(page=self)
            if navitems:
                navitems.delete()


class Section(models.Model):
    page = models.ForeignKey(Page,null=True,blank=True,help_text="The page this section belongs on.")
    slug = models.CharField("Short name",max_length=255,null=True,help_text="No spaces.")
    title = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    show_in_navigation = models.BooleanField(default=False)

    def __unicode__(self):
        return self.slug

    def save(self):
        super(Section, self).save()
        if self.show_in_navigation:
            navitem, created = NavigationItem.objects.get_or_create(section=self)
            navitem.slug=self.slug
            navitem.name=self.title
            navitem.section=self
            navitem.save()
        else:
            navitems = NavigationItem.objects.filter(section=self)
            if navitems:
                navitems.delete()


class Gallery(models.Model):
    name = models.CharField(max_length=255,null=True)
    image = models.ForeignKey('Photo',null=True,blank=True,related_name="main_img")

    class Meta:
        verbose_name_plural = 'galleries'

    def __unicode__(self):
        return self.name

    def photos(self):
        return Photo.objects.filter(gallery=self)


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery,null=True,blank=True)
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
            IMG_SIZE = (600,600)
            THUMBNAIL_SIZE = (100,100)

            thmb = Image.open(self.image)
            img = thmb.copy()

            if thmb.mode not in ('L', 'RGB'):
                thmb = thmb.convert('RGB')
                img = img.convert('RGB')

            thmb.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            img.thumbnail(IMG_SIZE, Image.ANTIALIAS)

            # Save the thumbnail
            temp_handle = StringIO()
            thmb.save(temp_handle, "JPEG")
            temp_handle.seek(0)
            img_handle = StringIO()
            img.save(img_handle, "JPEG")
            img_handle.seek(0)

            # Save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                    temp_handle.read())
            self.thumb.save(suf.name, suf, save=False)

            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                    img_handle.read())
            self.image.save(suf.name, suf, save=False)

        super(Photo, self).save()


class Article(models.Model):
    title = models.CharField(max_length=255,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    content = models.TextField(null=True,blank=True)
    image = models.ForeignKey(Photo,null=True,blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)


class Contact(models.Model):
    date = models.DateTimeField(auto_now_add=True,editable=False)
    first_name = models.CharField(max_length=255,null=True) # remove blank=True to require
    last_name = models.CharField(max_length=255,null=True)
#    company = models.CharField(max_length=255,null=True,blank=True)
#    title = models.CharField(max_length=255,null=True,blank=True)
#    address = models.CharField(max_length=255,null=True,blank=True)
#    address2 = models.CharField(max_length=255,null=True,blank=True)
#    city = models.CharField(max_length=255,null=True,blank=True)
#    state = models.CharField(max_length=255,null=True,blank=True)
#    zip_code = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
#    fax = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    message = models.TextField(null=True,blank=True)

    def to_msg(self):
        msg = ''
        if self.date:
            msg += 'Submitted on: ' + str(self.date)
        msg += '\nName: ' + self.first_name + ' ' + self.last_name
        if self.phone:
            msg += '\nPhone: ' + self.phone
        if self.email:
            msg += '\nEmail: ' + self.email
        if self.message:
            msg += '\nMessage: ' + self.message
        return msg



