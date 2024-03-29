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
from rest_framework.permissions import AllowAny
from django.shortcuts import render

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def retrieve(self, request, pk=None):
    user = get_object_or_404(User, pk=pk)
    frndStatus = getFriendStatus(request.user.id, user.id)
    serializer = UserSerializer(user, context={'request': request})
    data = serializer.data
    data['status'] = frndStatus
    return Response(data=data, status=status.HTTP_200_OK)
  #end

  def create(self, request):
    serializer = UserSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = serializer.data
    user = User.objects.get(username=data.get('username'))
    image = generateImage(user.email)
    serializer = UserProfileSerializer(data={'owner': user.id, 'image': image})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data['profile'] = serializer.data
    return Response(data=data, status=status.HTTP_200_OK)
  #end
#end

class GroupViewSet(viewsets.ModelViewSet):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
#end

class UserPostViewSet(viewsets.ModelViewSet):
  queryset = UserPost.objects.all()
  serializer_class = UserPostSerializer
#end

class GetPostLikes(APIView):
  def get(self, request, pk):
    likes = PostLike.objects.filter(post=pk)
    serializer = PostLikeSerializer(likes, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetPostComments(APIView):
  def get(self, request, pk):
    likes = PostComment.objects.filter(post=pk)
    serializer = PostCommentSerializer(likes, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end


class UserGroupViewSet(viewsets.ModelViewSet):
  queryset = UserGroup.objects.all()
  serializer_class = UserGroupSerializer

  def retrieve(self, request, pk=None):
    group = get_object_or_404(UserGroup, pk=pk)
    mberStatus = getMberSts(request.user.id, pk)
    serializer = UserGroupSerializer(group, context={'request': request})
    data = serializer.data
    data['status'] = mberStatus
    return Response(data=data, status=status.HTTP_200_OK)
  #end
#end

class GetUserFriends(APIView):
  def get(self, request, pk):
    user = get_object_or_404(User, pk=pk)
    queryset = getFriends(user.id)
    serializer = UserSerializer(queryset, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetUserPosts(APIView):
  def get(self, request, pk):
    user = get_object_or_404(User, pk=pk)
    queryset = UserPost.objects.filter(author=user.id)
    serializer = UserPostSerializer(queryset, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetUserProfile(APIView):
  def get(self, request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserProfileSerializer(user.profile, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetFriendMessages(APIView):
  def get(self, request, pk):
    messages = UserMessage.objects.filter(Q(sender=request.user, recver=pk)|Q(sender=pk, recver=request.user))
    serializer = UserMessageSerializer(messages, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class ChangeFriendStatus(APIView):
  def post(self, request, pk):
    friend = get_object_or_404(User, pk=pk)
    serializer = ActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    action = serializer.data.get('action')
    changeFrndSts(request.user, friend, action)
    return Response(status=status.HTTP_200_OK)
  #end
#end

class GetGroupMessages(APIView):
  def get(self, request, pk):
    messages = GroupMessage.objects.filter(group=pk)
    serializer = GroupMessageSerializer(messages, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end


class GetGroupMembers(APIView):
  def get(self, request, pk):
    members = getMembers(pk)
    serializer = UserSerializer(members, many=True, context={'request': request, 'admin': False})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetGroupPosts(APIView):
  def get(self, request, pk):
    posts = GroupPost.objects.filter(group=pk)
    serializer = UserPostSerializer(posts, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class GetGroupAdmins(APIView):
  def get(self, request, pk):
    members = getAdmins(pk)
    serializer = UserSerializer(members, many=True, context={'request': request, 'admin': True})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end


class GetGroupRequests(APIView):
  def get(self, request, pk):
    requests = getRequests(pk)
    serializer = UserSerializer(requests, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class ManageMyRequest(APIView):
  def post(self, request, pk):
    serializer = ActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    action = serializer.data.get('action')
    group = get_object_or_404(UserGroup, pk=pk)
    managJoinRequest(request.user, group, action)
    return Response(status=status.HTTP_200_OK)
  #end
#end

class ManageMemberRole(APIView):
  def post(self, request, pk):
    serializer = ManageMemberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    userId = serializer.data.get('user')
    user = get_object_or_404(User, pk=userId)
    group = get_object_or_404(UserGroup, pk=pk)
    admin = isGroupAdmin(request.user, group)
    if(admin is False):
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    #end
    action = serializer.data.get('action')
    mangMemberRole(user, group, action)
    return Response(status=status.HTTP_200_OK)
  #end
#end

class SignUp(APIView):
  permission_classes = (AllowAny,)
  def post(self, request):
    serializer = UserSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = serializer.data
    user = User.objects.get(username=data.get('username'))
    image = generateImage(user.email)
    serializer = UserProfileSerializer(data={'owner': user.id, 'image': image})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = Token.objects.create(user=user)
    return Response(data={'token': token.key}, status=status.HTTP_200_OK)
  #end
#end

class TokenLogout(APIView):
  def get(self, request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_200_OK)
  #end
#end