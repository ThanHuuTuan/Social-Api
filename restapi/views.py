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
#end

class GroupViewSet(viewsets.ModelViewSet):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
#end

class UserPostViewSet(viewsets.ModelViewSet):
  queryset = UserPost.objects.all()
  serializer_class = UserPostSerializer
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
    serializer = UserSerializer(members, many=True, context={'request': request})
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

class ManageJoinRequest(APIView):
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
    action = serializer.data.get('action')
    mangMemberRole(user, group, action)
    return Response(status=status.HTTP_200_OK)
  #end
#end

class SignUp(APIView):
  permission_classes = (AllowAny,)
  def post(self, request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    emailSerializer = EmailSerializer(data={'email': email})
    emailSerializer.is_valid(raise_exception=True)
    image = generateImage(emailSerializer.data.get('email'))
    serializer = UserSerializer(data={'profile': {'image': image}, 'username': username, 'email': email, 'password': password}, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  #end
#end

class TokenLogout(APIView):
  def get(self, request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_200_OK)
  #end
#end