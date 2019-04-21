from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

admin.site.register(UserPost)
admin.site.register(Session)