from django import forms
from django.core.validators import validate_integer
from .models import (Tag,
				Category,
				About_website,
				Contacted_Us,
				WebsitePage,
				WebProfile,
				Banner,
				EmailMarketingSignUp,
				EmailCampaignCategory,
				)

class FormLink:
	def __init__(self, text, url):
		self.name = text
		self.url = url


	def __str__(self):
		return self.name



class ExtraFormContext:

	def __init__(self, **kwargs):
		self.page_title = kwargs.get('page_title')
		self.form_title = kwargs.get('form_title ')
		self.form_method = kwargs.get('form_method')
		self.form_value = kwargs.get('form_value')
		self.form_action = kwargs.get('form_action')
		self.form_cancel = kwargs.get('form_cancel')
		self.form_links = kwargs.get('form_links')

	def get_context_data(cls, self, *args, **kwargs):
		context = super(cls, self).get_context_data(*args, **kwargs)
		context.update({'page_title' : self.page_title,
			'form_title' : self.form_title,
			'form_method': self.form_method,
			'form_value': self.form_value,
			'form_action': self.form_action,
			'form_cancel': self.form_cancel,
			'form_links': formlinks,
			})
		return context


class BsCharField(forms.CharField):

	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.TextInput(attrs = {'class': 'form-control'})
		super(BsCharField, self).__init__(*args, widget=widget, **kwargs)

class BsTextField(forms.CharField):

	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.Textarea(attrs = {'class': 'form-control', 'rows': '5'})
		super(BsTextField, self).__init__(*args, widget=widget, **kwargs)

class BsIntegerField(forms.IntegerField):

	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.NumberInput(attrs = {'class': 'form-control'})
		super(BsIntegerField, self).__init__(*args, widget=widget, **kwargs)

class BsPasswordField(forms.CharField):
	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.PasswordInput(attrs = {'class': 'form-control'})
		super(BsPasswordField, self).__init__(*args, widget=widget, **kwargs)

class BsEmailField(forms.EmailField):

	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.EmailInput(attrs = {'class': 'form-control'})
		super(BsEmailField, self).__init__(*args, widget=widget, **kwargs)

class BsChoiceField(forms.ChoiceField):

	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.Select(attrs = {'class': 'form-control'})
		super(BsChoiceField, self).__init__(*args, widget=widget, **kwargs)


class BsSlugField(forms.SlugField):
	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.TextInput(attrs = {'class': 'form-control'})
		super(BsSlugField, self).__init__(*args, widget=widget, **kwargs)

class BsBooleanField(forms.BooleanField):
	def __init__(self, *args, **kwargs):
		widget = kwargs.get('widget')
		if widget:
			widget.attrs['class'] += ' form-control'
		else:
			widget = forms.CheckboxInput(attrs = {'class': 'form-control'})
		super(BsBooleanField, self).__init__(*args, widget=widget, **kwargs)

# class BsEmailField(forms.EmailField):


class BsPhoneNumberField(BsCharField):
	def to_python(self, value):
		if not value:
			return []
		return int(value)

	def validate(self, value):
		super(BsPhoneNumberField, self).validate(value)
		validate_integer(value)
		if len(str(value)) < 8:
			raise forms.ValidationError("Enter a valid phone number")

class EmailMarketingSignUpForm(forms.ModelForm):
	subscriptions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=EmailCampaignCategory.objects.all())
	class Meta:
		model = EmailMarketingSignUp
		exclude = ['dateUpdated', 'dateCreated', 'active']





class ContactForm(forms.ModelForm):
	subject = BsCharField(max_length=30)
	name = BsCharField(max_length=30)
	email =BsEmailField()
	content = BsTextField(min_length = 10)

	class Meta:
		model = Contacted_Us
		exclude = ['dateUpdated', 'dateCreated', 'active', 'datePublished']

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ['dateUpdated' 'dateCreated','author', 'active']