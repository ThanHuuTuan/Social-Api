from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
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

  def list(self, request):
    queryset = self.get_queryset()
    serializer = UserPostSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)
  #end

  def get_queryset(self):
    queryset = UserPost.objects.all()
    authorName = self.request.query_params.get('author', None)
    if(authorName is not None):
      author = get_object_or_404(User, username=authorName)
      queryset = queryset.filter(author=author.id)
    #end
    return queryset
  #end

  def create(self, request):
    serializer = UserPostSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def retrieve(self, request, pk=None):
    post = get_object_or_404(UserPost, pk=pk)
    serializer = UserPostSerializer(post, context={'request': request})
    return Response(serializer.data)
  #end


  def update(self, request, pk=None):
    post = get_object_or_404(UserPost, pk=pk)
    serializer = UserPostSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    post = serializer.update(post, serializer.data)
    return Response(serializer.data)

  def partial_update(self, request, pk=None):
    pass

  def destroy(self, request, pk=None):
    pass
#end