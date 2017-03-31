from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.template import Template, Context

from core.functions import base_context
from . import tokenizer

class TokenizationProcess(View):
  def get(self, request):
    context = base_context(request)
    return render(request, 'tokenization_process.html', context)
    
def process_result(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
    'result': '',
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  text = request.POST.get('text')
  if not text:
    response['response'] = 'Ներմուծեք ինչ-որ տեքստ'
    return JsonResponse(response)
  
  try:
    T = tokenizer.Tokenizer(text)
    T.segmentation().tokenization()
    result = get_template('tokenization_output.html').render(Context({'segments': T.output()}))
  except Exception as E:
    response['response'] = 'Սխալմունք: {e}'.format(e)
    return JsonResponse(response)
  
  response = {
    'type': 'ok',
    'response': 'Մշակված է',
    'result': result,
  }
  return JsonResponse(response)