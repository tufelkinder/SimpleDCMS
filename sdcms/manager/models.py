import os
from django.db import models
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your models here.


class NavigationItem(models.Model):
    slug = models.CharField("Short name",max_length=255,null=True,help_text="No spaces.")
    name = models.CharField("Display name",max_length=255,null=True,blank=True)
    parent = models.ForeignKey('self',null=True,blank=True,help_text="Leaving this blank creates a new navigation option which may affect the layout of the site.")
    page = models.ForeignKey('Page',null=True,blank=True)
    link = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to="img/nav/",blank=True,null=True)
    rollover = models.ImageField(upload_to="img/nav/",blank=True,null=True)
    order = models.IntegerField(null=True,blank=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.slug

    def children(self):
        return NavigationItem.objects.filter(parent=self)


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

    def save(self):
        if self.show_in_navigation:
            if not NavigationItem.objects.filter(page=self):
                navitem = NavigationItem(slug=self.slug,
                                         name=self.title,
                                         page=self)
                navitem.save()
        else:
            navitems = NavigationItem.objects.filter(page=self)
            if navitems:
                navitems.delete()
        super(Page, self).save()


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
            self.image.save(suf.name, suf, save=False)

        super(Article, self).save()


class Contact(models.Model):
    date = models.DateTimeField(auto_now_add=True,editable=False)
    first_name = models.CharField(max_length=255,null=True) # remove blank=True to require
    last_name = models.CharField(max_length=255,null=True)
    company = models.CharField(max_length=255,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    address2 = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    zip_code = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    fax = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)

    def to_msg(self):
        msg = ''
        if self.date:
            msg += 'Submitted on: ' + str(self.date)
        msg += '\nName: ' + self.first_name + ' ' + self.last_name
        if self.company:
            msg += '\nCompany: ' + self.company
        if self.title:
            msg += '\nTitle: ' + self.title
        if self.address:
            msg += '\nAddress: ' + self.address
        if self.address2:
            msg += '\nAddress 2: ' + self.address2
        if self.city:
            msg += '\nCity: ' + self.city
        if self.state:
            msg += ', ' + self.state
        if self.zip_code:
            msg += ' ' + self.zip_code
        if self.phone:
            msg += '\nPhone: ' + self.phone
        if self.fax:
            msg += '\nFax: ' + self.fax
        if self.email:
            msg += '\nEmail: ' + self.email
        return msg



