
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
import hashlib


class UserPost(models.Model):
  content = models.CharField(
    max_length=1000
  )
  author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='posts'
  )
  image = models.CharField(
    max_length=1000, 
  )
  publish = models.DateField(
    default=date.today
  )
  def __str__(self):
    return self.content[:50]
  #end
#end

class PostLike(models.Model):
  owner = models.ForeignKey(User, 
    related_name='galngkeng',
    on_delete=models.CASCADE
  )
  post = models.ForeignKey(UserPost,
    related_name='likes',
    on_delete=models.CASCADE
  )
  date = models.DateField(
    default=date.today
  )
#end


class PostComment(models.Model):
  owner = models.ForeignKey(User, 
    related_name='genglandkd',
    on_delete=models.CASCADE
  )
  post = models.ForeignKey(UserPost,
    related_name='comments',
    on_delete=models.CASCADE
  )
  content = models.CharField(
    max_length=1000
  )
  date = models.DateField(
    default=date.today
  )
#end

class Friendship(models.Model):
  owner = models.ForeignKey(User, 
    related_name='friendship',
    on_delete=models.CASCADE
  )
  friend = models.ForeignKey(User, 
    on_delete=models.CASCADE,
    related_name='lgougolfgo'
  )
  date = models.DateField(
    default=date.today
  )
#end


class FriendRequest(models.Model):
  recver = models.ForeignKey(User,
    related_name='reqrcvd',
    on_delete=models.CASCADE
  )
  sender = models.ForeignKey(User,
    related_name='reqsent',
    on_delete=models.CASCADE
  )
  time = models.DateTimeField(
    default=datetime.now,
  )
#end


class UserProfile(models.Model):
  owner = models.OneToOneField(User,
    on_delete=models.CASCADE,
    related_name='profile'
  )
  image = models.URLField(
    max_length=100
  )
  about = models.CharField(
    max_length=100,
    default='Hi, I am a new User'
  )
  def __str__(self):
    return self.owner.username
  #end
#end


class UserMessage(models.Model):
  sender = models.ForeignKey(User,
    on_delete=models.CASCADE,
    related_name='aohgaldeng',
  )
  recver = models.ForeignKey(User,
    on_delete=models.CASCADE,
    related_name='qogbgakend'
  )
  content = models.CharField(
    max_length=1000,
    null=False
  )
  time = models.DateTimeField(
    default=datetime.now
  )
  seen = models.BooleanField(
    default=False
  )
#end


class UserGroup(models.Model):
  name = models.CharField(
    max_length=100
  )
  created = models.DateField(
    default=date.today
  )
  type = models.CharField(
    max_length=20,
    choices=(('public', 'Public'), ('private', 'Private'), ('secret', 'Secret')),
    default='private'
  )
  image = models.URLField(
    max_length=100
  )
  def __str__(self):
    return self.name
  #end
#end


class GroupPost(models.Model):
  content = models.CharField(
    max_length=1000
  )
  group = models.ForeignKey(UserGroup,
    on_delete=models.CASCADE,
    related_name='posts'
  )
  author = models.ForeignKey(User,
    on_delete=models.CASCADE,
    related_name='lahjgkengll'
  )
  image = models.CharField(
    max_length=1000, 
  )
  publish = models.DateField(
    default=date.today
  )
  def __str__(self):
    return self.content[:50]
  #end
#end


class GroupMember(models.Model):
  owner = models.ForeignKey(User,
    on_delete=models.CASCADE,
    related_name='usergroup'
  )
  group = models.ForeignKey(UserGroup,
    on_delete=models.CASCADE,
    related_name='members'
  )
  time = models.DateField(
    default=date.today
  )
  admin = models.BooleanField(
    default=False
  )
  def __str__(self):
    return self.owner.username
  #end
#end


class GroupRequest(models.Model):
  group = models.ForeignKey(UserGroup,
    related_name='requests',
    on_delete=models.CASCADE
  )
  sender = models.ForeignKey(User,
    related_name='olgoufuf',
    on_delete=models.CASCADE
  )
  time = models.DateTimeField(
    default=datetime.now,
  )
  def __str__(self):
    return self.group.name
  #end
#end

class GroupMessage(models.Model):
  sender = models.ForeignKey(User,
    on_delete=models.CASCADE,
    related_name='agahdgapegn'
  )
  group = models.ForeignKey(UserGroup,
    on_delete=models.CASCADE,
    related_name='messages'
  )
  content = models.CharField(
    max_length=1000
  )
  time = models.DateTimeField(
    default=datetime.now
  )
  seen = models.BooleanField(
    default=False
  )
  def __str__(self):
    return self.group.name
  #end
#end


#Helping functions for views
def getFriends(user):
  friendships = Friendship.objects.filter(owner=user).order_by('date')
  friends = [friendship.friend for friendship in friendships]
  return friends
#end

def generateImage(email):
  hash = hashlib.md5(email.encode("utf-8")).hexdigest()
  image = 'http://gravatar.com/avatar/'+hash+'?s=200&d=retro'
  return image
#end

def getAllGroups(user):
  memberships = GroupMember.objects.filter(owner=user)
  groups = [member.group for member in memberships]
  return groups
#end

def getMembers(group):
  memberships = GroupMember.objects.filter(group=group)
  members = [membership.owner for membership in memberships]
  return members
#end

def isGroupAdmin(user, group):
  admin = GroupMember.objects.filter(owner=user, group=group, admin=True).count()
  return admin != 0
#end

def getAdmins(group):
  memberships = GroupMember.objects.filter(group=group, admin=True)
  members = [membership.owner for membership in memberships]
  return members
#end

def getRequests(group):
  requests = GroupRequest.objects.filter(group=group)
  return [request.sender for request in requests]
#end


def getFriendStatus(user, friend):
  isFriend = Friendship.objects.filter(owner=user, friend=friend).count()
  reqsent = FriendRequest.objects.filter(sender=user, recver=friend).count()
  reqrcvd = FriendRequest.objects.filter(sender=friend, recver=user).count()
  if(id(user) == id(friend)):
    return 'thiself'
  elif(isFriend):
    return 'friend'
  elif(reqsent):
    return 'reqsent'
  elif(reqrcvd):
    return 'reqrcvd'
  else:
    return 'notfrnd'
  #end
#end

def changeFrndSts(user, friend, action):
  if(action == 'delfriend'):
    Friendship.objects.filter(owner=user, friend=friend).delete()
    Friendship.objects.filter(owner=friend, friend=user).delete()
  elif(action == 'sendrqust'):
    FriendRequest.objects.create(sender=user, recver=friend)
  elif(action == 'delsntrqst'):
    FriendRequest.objects.filter(sender=user, recver=friend).delete()
  elif(action == 'acptrequst'):
    Friendship.objects.create(owner=user, friend=friend)
    Friendship.objects.create(owner=friend, friend=user)
    FriendRequest.objects.filter(sender=friend, recver=user).delete()
  elif(action == 'delrcvdrqst'):
    FriendRequest.objects.filter(sender=friend, recver=user).delete()
  #end
#end


def getMberSts(user, group):
  sntrqst = GroupRequest.objects.filter(sender=user, group=group).count()
  try:
    member = GroupMember.objects.get(owner=user, group=group)
  except Exception as e:
    member = False
  if(member):
    return {"member": True, "admin": member.admin, "sntrqst": False}
  elif(sntrqst):
    return {"member": False, "admin": False, "sntrqst": True}
  else:
    return {"member": False, "admin": False, "sntrqst": False}
  #end
#end


def managJoinRequest(user, group, action):
  if(action == 'sendrqust'):
    GroupRequest.objects.create(sender=user,group=group)
  elif(action == 'delsntrqust'):
    GroupRequest.objects.filter(sender=user,group=group).delete()
  elif(action == 'leavegroup'):
    GroupMember.objects.filter(owner=user, group=group).delete()
  #end
#end


def mangMemberRole(user, group, action):
  if(action == 'delmember'):
    GroupMember.objects.filter(owner=user, group=group).delete()
  elif(action == 'addmember'):
    GroupRequest.objects.filter(sender=user,group=group).delete()
    GroupMember.objects.create(owner=user, group=group)
  elif(action == 'delrequest'):
    GroupRequest.objects.filter(sender=user, group=group).delete()
  #end
#end