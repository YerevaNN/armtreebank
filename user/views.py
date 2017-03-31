from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View

from .models import UserProfile
from .forms import LoginForm
from core.functions import base_context

def user_login(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք"
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if request.user.is_authenticated:
    response['response'] = 'Արդեն գրանցված եք'
    return JsonResponse(response)
  
  form = LoginForm(request.POST)
  if not form.is_valid():
    response['response'] = 'Լրացրեք տվյալները'
    return JsonResponse(response)
  
  try:
    usr = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    login(request, usr)
  except Exception:
    response['response'] = "Գաղտնաբառը և մուտքանունը չեն համապատասխանում"
    return JsonResponse(response)
    
  response = {
    'type': 'ok',
    'response': "Դուք մուտք գործեցիք:",
    'id': UserProfile.objects.get(user=request.user).id
  }
  return JsonResponse(response)
  
def user_logout(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք"
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  logout(request)
  return JsonResponse({ 
    'type': 'ok',
    'response': 'Դուք դուրս եկաք' 
  })

