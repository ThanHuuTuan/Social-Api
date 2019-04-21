from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('url', 'username', 'email', 'groups')
  #end


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('url', 'name')
  #end


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=20)
  password = serializers.CharField(max_length=50)
#end


class UserPostSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = UserPost 
    fields = ('content', 'author', 'image', 'publish')
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