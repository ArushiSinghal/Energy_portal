from __future__ import unicode_literals
from django.contrib import admin
from .models import Googlenews
from .models import Querynews
from .models import Photo
from .models import UploadIdea,Comment,Like
admin.site.register(Photo)
admin.site.register(Googlenews)
admin.site.register(Querynews)
admin.site.register(UploadIdea)
admin.site.register(Comment)
admin.site.register(Like)

# Register your models here.
