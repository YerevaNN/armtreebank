from user.forms import LoginForm
from user.models import UserProfile

from tokenization.forms import FEATURE_FORMS, NounParserForm, NounManualForm, VerbParserForm, VerbManualForm

def base_context(request):
  
  context = {
    'login_form': LoginForm(),
    'auth': request.user.is_authenticated,
    'user': UserProfile.objects.get(user=request.user) if request.user.is_authenticated else False,
    'feature_form_templates': FEATURE_FORMS,
    'noun_feature_form': {'parser': NounParserForm,
                          'manual': NounManualForm,
                           },
    'verb_feature_form': {'parser': VerbParserForm,
    					            'manual': VerbManualForm,
    					             },
  }
  
  return context