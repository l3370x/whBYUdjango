from django.db import models
from django.contrib.auth.models import User
from django import forms

class News(models.Model):
  def __unicode__(self):
    return self.first_name
  def name(self):
      return self.first_name + ' ' + self.last_name
  user = models.ForeignKey(User, editable=False)
  title = models.CharField(max_length=200)
  message = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  
  
class NewsForm(forms.ModelForm):
  class Meta:
    model = News
