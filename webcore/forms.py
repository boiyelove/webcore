from django import forms
from .models import EmailMarketingSignUp, Contact
from django.forms import ModelForm

class NewsletterForm(ModelForm):
	class Meta:
		model = EmailMarketingSignUp
		exclude = ['updated', 'created', 'active']

class ContactForm(ModelForm):
	class Meta:
		model = Contact
		exclude = ['updated', 'created']