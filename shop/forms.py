from dataclasses import field, fields
from pyexpat import model
from django import forms
from .models import Product



class StateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(StateForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = Product
		fields = ['state']
		widgets = {'state': forms.Select(attrs={'class':'form-select bg-white','style':'border: 1px solid #1A4953;font-size:14px;'})}

