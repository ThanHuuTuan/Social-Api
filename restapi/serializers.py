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
  profile = UserProfileSerializer(required=False)
  class Meta:
    model = User
    fields = ('url', 'profile', 'username', 'email')
  #end

  def create(self, validated_data):
    profile_data = validated_data.pop('profile')
    print(validated_data)
    user = User.objects.create(**validated_data)
    UserProfile.objects.create(owner=user, **profile_data)
    return user
  #end
#end


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('url', 'name')
  #end

class UserPostSerializer(serializers.HyperlinkedModelSerializer):
  author = UserSerializer(required=False)
  class Meta:
    model = UserPost 
    fields = ('url', 'author', 'content', 'image', 'publish')
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