from django.db import models
from django.contrib.auth.models import User
from datetime import date

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