from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from account.models import Account
#class RegisterForm(UserCreationForm):
#	email= forms.EmailField(max_length=60,help_text='Required. Add a valid Email address')
#	class Meta:
#		model = User
#		fields = ["email","name", "contact_number", "password"]

class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model =Account
		fields=('email','password')

	def clean(self):
		email=self.cleaned_data['email']
		password=self.cleaned_data['password']
		if not authenticate(email=email, password=password):
			raise forms.ValidationError("Invalid Login")


class blogger_registeration(forms.Form):
    title = forms.CharField(label='Title', max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea , max_length=2000)
