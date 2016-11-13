from django import forms
from django.forms import ModelForm
from .models import (Tag,
				Category,
				About_website,
				Contacted_Us,
				WebsitePage,
				WebProfile,
				Banner,
				EmailMarketingSignUp,
				EmailMarketingConfirmed
				)


class EmailMarketingSignUpForm(ModelForm):
	class Meta:
		model = EmailMarketingSignUp
		exclude = ['updated_on', 'created_on', 'active']

	def clean(self, *args, **kwargs):
		return form

class ContactForm(ModelForm):
	class Meta:
		model = Contacted_Us
		exclude = ['updated_on', 'created_on', 'active']

class CategoryForm(ModelForm):
	class Meta:
		model = Category
		exclude = ['updated_on', 'created_on', 'author', 'active']