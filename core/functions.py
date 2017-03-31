from user.forms import LoginForm
from user.models import UserProfile

def base_context(request):
  
  context = {
    'login_form': LoginForm(),
    'auth': request.user.is_authenticated,
    'user': UserProfile.objects.get(user=request.user) if request.user.is_authenticated else False,
  }
  
  return context