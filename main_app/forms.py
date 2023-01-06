
from django.forms import ModelForm
from .models import Unmasked

class UnmaskedForm(ModelForm):
  class Meta:
    model = Unmasked
    fields = ['date', 'masks']
