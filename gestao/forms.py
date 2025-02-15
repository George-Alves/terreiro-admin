# gestao/forms.py
from django import forms
from .models import Cargo, Hierarquia

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nome']

class HierarquiaForm(forms.ModelForm):
    class Meta:
        model = Hierarquia
        fields = ['nome']