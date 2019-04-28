from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

admin.site.register(UserPost)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
admin.site.register(UserProfile)
admin.site.register(UserMessage)
admin.site.register(UserGroup)
admin.site.register(GroupMember)
admin.site.register(GroupRequest)
admin.site.register(GroupMessage)
admin.site.register(Session)