from django import forms
from ckeditor.widgets import CKEditorWidget

# creating a form
class AddproductForm(forms.Form):
	short_desc = forms.CharField(label='Short Description',widget=CKEditorWidget(attrs={'rows':'3','required':'required'}))
	desc = forms.CharField(label='Description', widget=CKEditorWidget(attrs={'required':'required'}))