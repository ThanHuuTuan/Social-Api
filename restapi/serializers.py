from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from datetime import date
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
  class Meta:
    model = UserProfile 
    fields = ('id', 'owner', 'image', 'about')
  #end
#end

class UserSerializer(serializers.HyperlinkedModelSerializer):
  profile = UserProfileSerializer(read_only=True)
  class Meta:
    model = User
    fields = ('id', 'url', 'profile', 'password', 'username', 'email')
    extra_kwargs = {'password': {'write_only': True}}
  def create(self, validated_date):
    user = User(**validated_date)
    user.set_password(validated_date['password'])
    user.save()
    return user
  #end
#end


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('id', 'url', 'name')
  #end

class UserPostSerializer(serializers.HyperlinkedModelSerializer):
  author = UserSerializer(read_only=True)
  class Meta:
    model = UserPost 
    fields = ('id', 'url', 'author', 'content', 'image', 'publish')

  def create(self, validated_date):
    validated_date['author'] = self.context['request'].user
    post = UserPost.objects.create(**validated_date)
    return post
  #end
#end

class UserMessageSerializer(serializers.HyperlinkedModelSerializer):
  sender = UserSerializer(read_only=True)
  recver = UserSerializer(read_only=True)
  class Meta:
    model = UserMessage 
    fields = ('id', 'sender', 'recver', 'content', 'time', 'seen')
  #end
#end


class GroupMessageSerializer(serializers.HyperlinkedModelSerializer):
  sender = UserSerializer(read_only=True)
  class Meta:
    model = GroupMessage 
    fields = ('id', 'sender', 'group', 'content', 'time', 'seen')
  #end
#end

class UserGroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = UserGroup
    fields = ('id', 'url', 'name', 'created', 'type', 'image')
  #end
#end

class ActionSerializer(serializers.Serializer):
  action = serializers.CharField(max_length=20)
#end


class ManageMemberSerializer(serializers.Serializer):
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
  action = serializers.CharField(max_length=20)
#end

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=20)
  password = serializers.CharField(max_length=20, style={'input_type': 'password'})
#end

class EmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=50)
#end