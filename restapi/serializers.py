from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = UserProfile 
    fields = ('image', 'about')
  #end
#end

class UserSerializer(serializers.HyperlinkedModelSerializer):
  profile = UserProfileSerializer()
  class Meta:
    model = User
    fields = ('url', 'profile', 'username', 'email')
  #end


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('url', 'name')
  #end

class UserPostSerializer(serializers.HyperlinkedModelSerializer):
  author = UserSerializer()
  class Meta:
    model = UserPost 
    fields = ('url', 'author', 'content', 'image', 'publish')
  #end
  def create(self, validate_data):
    post = UserPost.objects.create(**validate_data)
    return post
  #end
  def update(self, instance, validate_data):
    instance.content = validate_data.get('content', instance.content)
    instance.image = validate_data.get('image', instance.image)
    instance.save()
    return instance
  #end
#end

class UserMessageSerializer(serializers.HyperlinkedModelSerializer):
  sender = UserSerializer()
  recver = UserSerializer()
  class Meta:
    model = UserMessage 
    fields = ('sender', 'recver', 'content', 'time', 'seen')
  #end
#end


class GroupMessageSerializer(serializers.HyperlinkedModelSerializer):
  sender = UserSerializer()
  class Meta:
    model = GroupMessage 
    fields = ('sender', 'group', 'content', 'time', 'seen')
  #end
#end

class UserGroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = UserGroup
    fields = ('url', 'name', 'created', 'type', 'image')
  #end
#end
