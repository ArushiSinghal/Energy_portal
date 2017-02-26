from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.validators import RegexValidator
from django.utils.encoding import python_2_unicode_compatible
import datetime, os, sys
#from PIL import Image
from django.core.files import File
from django.conf import settings
#from tinymce.models import HTMLField
from django import forms
#from tinymce.widgets import TinyMCE
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UploadIdea(models.Model):
	uploader = models.ForeignKey('auth.User')
	title = models.CharField(max_length=800 , default="Title")	
	upload_image = models.FileField(upload_to='photos',null=True)
	date = models.DateTimeField(default=timezone.now)
        bio = models.TextField(max_length=3000, default = "About You")
	content = models.TextField(max_length=3000 , default = "Your Idea")
	link = models.CharField(max_length=600,null=True)
        
        def __str__(self):
             return self.title
        def approved_comments(self):
             return self.comments.filter(approved_comment=True)




@python_2_unicode_compatible
class Googlenews(models.Model):
	title = models.CharField(max_length=512)
        original_url = models.CharField(max_length=1024)
        pubdate = models.DateTimeField()
        imageurl = models.CharField(max_length=512,null=True)
        description = models.TextField()
        pub_agency = models.CharField(max_length=512)
	def __str__(self):
        	return self.title
class Querynews(models.Model):
	query = models.CharField(max_length=300)
        num = models.IntegerField()
        def __str__(self):
        	return self.query

class Photo(models.Model):
        title = models.CharField(max_length=250,
                help_text='Maximum 250 characters.', blank=True)
        slug = models.SlugField(unique = True,
                help_text='Suggested value automatically generated from title. Must be unique.', null=True)
        caption = models.TextField(blank=True, max_length=250,
                help_text='An optional summary.')
        date = models.DateTimeField(default=timezone.now)
        image = models.ImageField(upload_to='photos',
                help_text=mark_safe("Kindly optimize the image <a href='http://optimizilla.com/'>here</a> before uploading"))

        class Meta:
                ordering = ['-date']
        def __unicode__(self):
                return self.title

        def get_absolute_url(self):
                return ('thaddeus_photo_detail', (),
                                { 'slug': self.slug })
        get_absolute_url = models.permalink(get_absolute_url)


class Comment(models.Model):
    post = models.ForeignKey('UploadIdea', related_name='comments')
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.ForeignKey('auth.User')
    like_article = models.ForeignKey('UploadIdea', related_name='likes')
    created_date = models.DateTimeField(default=timezone.now)
