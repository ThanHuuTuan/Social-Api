from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

admin.site.register(UserPost)
admin.site.register(Friendship)
admin.site.register(UserRequest)
admin.site.register(UserProfile)
admin.site.register(UserMessage)
admin.site.register(UserGroup)
admin.site.register(GroupMember)
admin.site.register(GroupRequest)
admin.site.register(GroupMessage)
admin.site.register(Session)