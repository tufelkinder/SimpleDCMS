from django.db import models

# Create your models here.


class NavigationItem(models.Model):
    name = models.CharField("Short name",max_length=255,null=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    page = models.ForeignKey(Page,null=True,blank=True)
    link = models.CharField(max_length=255,null=True,blank=True)
    order = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(max_length=255,null=True)
    html = models.FileField(upload_to='templ',null=True,blank=True)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=255,null=True)
    content = models.TextField(null=True,blank=True)
    template = models.ForeignKey(Template,null=True,blank=True,help_text="Leave empty to use standard 'page.html' template.")

    def __unicode__(self):
        return self.name


class Element(models.Model):
    name = models.CharField(max_length=255,null=True)
    content = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return self.name


class Graphic(models.Model):
    name = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='img',null=True,blank=True)
    thumb = models.ImageField(upload_to='img/thumb',null=True,blank=True)

    def __unicode__(self):
        return self.name


    