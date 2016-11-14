from django import forms
from .models import (Tag,
				Category,
				About_website,
				Contacted_Us,
				WebsitePage,
				WebProfile,
				Banner,
				EmailMarketingSignUp,
				EmailVerification
				)


class EmailVerificationForm(forms.ModelForm):
	class Meta:
		model = EmailVerification
		exclude = [	'slug', 'confirmed', 'updated_on', 'created_on' ]


class EmailMarketingSignUpForm(forms.ModelForm):
	class Meta:
		model = EmailMarketingSignUp
		exclude = ['updated_on', 'created_on', 'active']











class ContactForm(forms.ModelForm):
	class Meta:
		model = Contacted_Us
		exclude = ['updated_on', 'created_on', 'active']

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ['updated_on', 'created_on', 'author', 'active']