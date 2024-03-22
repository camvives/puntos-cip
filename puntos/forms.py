from django import forms
from .models import Entrada

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['fecha', 'tipo_oracion', 'seccion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input type
        }