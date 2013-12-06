from django import forms

class RegisterForm(forms.Form):
	main = forms.URLField(max_length = 255, label = "Your steam profile URL");