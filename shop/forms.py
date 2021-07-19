from django import forms
from ckeditor.widgets import CKEditorWidget

# creating a form
class AddproductForm(forms.Form):
	short_desc = forms.CharField(label='Short Description',widget=CKEditorWidget())
	desc = forms.CharField(label='Description', widget=CKEditorWidget())