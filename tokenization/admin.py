from django.contrib import admin

from .models import *

admin.site.register(Sentence)
admin.site.register(Token)

admin.site.register(NounAnimacy)


class WordAdmin(admin.ModelAdmin):
  list_display = ('word', 'pos' )
  list_filter = ('pos', )
  ordering = ('-creation_date',)
  search_fields = ['word']
admin.site.register(Word, WordAdmin)

class VerbAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Verb, VerbAdmin)

class PunctAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Punct, PunctAdmin)

class SymAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Sym, SymAdmin)

class XAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(X, XAdmin)

class IntjAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Intj, IntjAdmin)

class AdjAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Adj, AdjAdmin)

class AdvAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Adv, AdvAdmin)

class CconjAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Cconj, CconjAdmin)

class SconjAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Sconj, SconjAdmin)

class AuxAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Aux, AuxAdmin)

class PronAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Pron, PronAdmin)

class DetAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Det, DetAdmin)

class AdpAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Adp, AdpAdmin)

class PartAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Part, PartAdmin)

class NumeralAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Numeral, NumeralAdmin)

class NounAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False
admin.site.register(Noun, NounAdmin)