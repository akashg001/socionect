from django.contrib import admin
from .models import userprofile, posts,Message
# Register your models here.
admin.site.register(userprofile)
admin.site.register(posts)
admin.site.register(Message)
