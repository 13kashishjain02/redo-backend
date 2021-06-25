from django import forms
from ckeditor.widgets import CKEditorWidget

# creating a form
class AddproductForm(forms.Form):
	desc = forms.CharField(label='Description',widget=CKEditorWidget())