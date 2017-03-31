from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  
  def get_full_name(self):
    return '{} {}'.format( self.user.first_name, self.user.last_name )
  
  def __str__(self):
    return self.get_full_name()
