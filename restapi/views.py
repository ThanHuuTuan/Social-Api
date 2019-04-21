from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from rest_framework import viewsets
from .serializers import *
from .models import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows groups to be viewed or edited.
  """
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
#end

class TokenLogout(APIView):
  def get(self, request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_200_OK)
  #end

class UserPostViewSet(viewsets.ModelViewSet):
  queryset = UserPost.objects.all()
  serializer_class = UserPostSerializer
#end

class UserGroupViewSet(viewsets.ModelViewSet):
  queryset = UserGroup.objects.all()
  serializer_class = UserGroupSerializer
#end

class GetUserFriends(APIView):
  def get(self, request, username):
    user = get_object_or_404(User, username=username)
    queryset = getFriends(user.id)
    serializer = UserSerializer(queryset, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end

class GetUserPosts(APIView):
  def get(self, request, username):
    user = get_object_or_404(User, username=username)
    queryset = UserPost.objects.filter(author=user.id)
    serializer = UserPostSerializer(queryset, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end

class GetUserProfile(APIView):
  def get(self, request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserProfileSerializer(user.profile, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetFriendMessages(APIView):
  def get(self, request, friend):
    friend = get_object_or_404(User, username=friend)
    messages = UserMessage.objects.filter(Q(sender=request.user, recver=friend)|Q(sender=friend, recver=request.user))
    serializer = UserMessageSerializer(messages, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetGroupMessages(APIView):
  def get(self, request, pk):
    group = get_object_or_404(UserGroup, pk=pk)
    messages = GroupMessage.objects.filter(group=group)
    serializer = GroupMessageSerializer(messages, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end