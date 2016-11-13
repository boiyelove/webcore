from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import ContactForm, NewsletterForm



#Default Website Pages
	#templates at _dwp/
class HomePageView(TemplateView):
	template_name = "_dwp/home.html"


class AboutUsPageView(TemplateView):
	template_name = "_dwp/aboutus.html"


class ContactUsPageView(TemplateView):
	template_name = "_dwp/contactus.html"


class PageView(TemplateView):
	template_name = "_dwp/page.html"



#Custom Error Pages
	#templates at _cep/
def handler400(request):
	template = '_cep/400.html'
	context = {}
	return render(request, template, context)

def handler403(request):
	template = '_cep/403.html'
	context = {}
	return render(request, template, context)

def handler404(request):
	template = '_cep/404.html'
	context = {}
	return render(request, template, context)

def handler500(request):
	template = '_cep/500.html'
	context = {}
	return render(request, template, context)




#Default Webste Apps
	#templates at _dwa/
def newsletter_signup(request):
	source = request.META.get('HTTP_REFERER')
	news_signup = NewsletterForm(request.POST or None)
	if news_signup.is_valid():
		email = news_signup.clean_data.get('email')
		obj, created = EmailMarketingSignUp.objects.get_or_create(email = email)
		if created:
			messages.success(request, "You are now on our list, you'll hear from us from time to time")
		elif not created and obj:
			messages.success(request, "You already subscribed to our list. We'll now send you updates")
		else:
			messages.error(request, "Oh! something went wrong. Sorry about that.")
	else:
		messages.error(request, "Oh! something went wrong. Sorry about that.")
	return HttpResponseRedirect(source)


def contact(request):
	new_contact = ContactForm(request.POST or None)
	if new_contact.is_valid():
		new_contact.save()
		messages.success(request, "Thank you for contacting us, we'll reply to your enquiry as soon as we can")
		return HttpResponseRedirect('/')
	if new_contact.errors:
		messages.warning(request, "Sorry Something went wrong")
	template = 'contact.html'
	context = {'contactform' : new_contact}
	return render(request, template, context)