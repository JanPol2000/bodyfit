from django import forms
from .models import *

class ClientesForm(forms.ModelForm):
	class Meta:
		model = Clientes 
		fields = '__all__'

class MembresiaForm(forms.ModelForm):
	class Meta:
		model = Membresia 
		fields = '__all__'