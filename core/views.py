from django.shortcuts import render, redirect
from django.views import View

from user.models import UserProfile
from .functions import base_context

class HomePageView(View):
  
  def get(self, request):
    return render(request, 'home.html', base_context(request))

class AboutPageView(View):

  def get(self, request):
    return render(request, 'about.html', base_context(request))
