
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


class UserRequest(models.Model):
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


def getFriendStatus(user, friend):
  friend = Friendship.objects.filter(owner=user, friend=friend).count()
  reqsent = UserRequest.objects.filter(sender=user, recver=friend).count()
  reqrcvd = UserRequest.objects.filter(sender=friend, recver=user).count()
  if(friend):
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
    UserRequest.objects.create(sender=user, recver=friend)
  elif(action == 'delsntrqst'):
    UserRequest.objects.filter(sender=user, recver=friend).delete()
  elif(action == 'acptrequst'):
    Friendship.objects.create(owner=user, friend=friend)
    Friendship.objects.create(owner=friend, friend=user)
    UserRequest.objects.filter(sender=friend, recver=user).delete()
  elif(action == 'delrcvdrqst'):
    UserRequest.objects.filter(sender=friend, recver=user).delete()
  #end
#end


def getMberSts(user, group):
  sntrqst = GroupRequest.objects.filter(sender=user, group=group).count()
  try:
    member = GroupMember.objects.get(owner=user, group=group)
  except Exception as e:
    member = False
  #end
  if(member):
    return {"member": True, "admin": member.admin, "sntrqst": False, "notmber": False}
  elif(sntrqst):
    return {"member": False, "admin": False, "sntrqst": True, "notmber": False}
  else:
    return {"member": False, "admin": False, "sntrqst": False, "notmber": True}
  #end
#end


def changeMemberRole(user, group, action):
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