from django import forms
from ckeditor.widgets import CKEditorWidget

class add_blog(forms.Form):
    title = forms.CharField(label='Title', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content = forms.CharField(widget=forms.Textarea , max_length=2000)
    content = forms.CharField(widget = CKEditorWidget())
    image= forms.ImageField(required=False,widget=forms.widgets.ClearableFileInput())