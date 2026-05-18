from django.contrib import admin
from .models import Notification, Post

admin.site.register(Post)
admin.site.register(Notification)

