from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import (ContactForm, 
					EmailMarketingSignUpForm,
					CategoryForm
					)
from django.urls import reverse_lazy
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


#Custom Error Pages
	#templates at _cep/
def handler400(request):
	template = 'webcore/_cep/400.html'
	context = {}
	return render(request, template, context)

def handler403(request):
	template = 'webcore/_cep/403.html'
	context = {}
	return render(request, template, context)

def handler404(request):
	template = 'webcore/_cep/404.html'
	context = {}
	return render(request, template, context)

def handler500(request):
	template = 'webcore/_cep/500.html'
	context = {}
	return render(request, template, context)






#Default Website Pages
	#templates at _dwp/
class HomePageView(TemplateView):
	template_name = "webcore/_dwp/home.html"


class AboutUsPageView(TemplateView):
	template_name = "webcore/_dwp/aboutus.html"


class ContactUsPageView(TemplateView):
	template_name = "webcore/_dwp/contactus.html"


class PageView(TemplateView):
	template_name = "webcore/_dwp/page.html"






#Default Webste Apps
	#templates at _dwa/

#Category App
class CategoryView:
	form_class = CategoryForm
	success_url = reverse_lazy("webcore/_dwa/category-detail")
	
class CreateCategory(CategoryView, CreateView):

	def get_context_data(*args, **kwargs):
		context = super(CreateCategory, self).get_context_data(**kwargs)
		context['head_title'] = "Create New Category"
		context["page_title"] = "Create New category"
		context["btn_title"] = "Create Category"
		return context

class UpdateCatgory(CategoryView, UpdateView):
	
	def get_context_data(*args, **kwargs):
		context = super(CreateCategory, self).get_context_data(**kwargs)
		context['head_title'] = "Update Category"
		context["page_title"] = "Update category"
		context["btn_title"] = "Update Category"
		return context


class CategoryDelete(DeleteView):
	model = Category
	success_url = reverse_lazy("webcore/_dwa/category-list")

class CategoryList(ListView):
	model = Category
	template_name = "webcore/_dwa/category_list.html"

class CategoryDetail(DetailView):
	model = Category
	template_name = "webcore/_dwa/category_detail.html"



#Pages App
class AddWebsitePage(CreateView):
	pass











#Newsletter App
class AddEmailToCampaignList(View):
	template_name = "webcore/form.html"
	success_url = reverse_lazy("thank-you")

	def get(request, *args, **kwargs):
		form = EmailMarketingSignUpForm()

		return render(request, template_name, context)

	def post(request, *args, **kwargs):
		return render(request, template, context)
		
	def get_context_data(self, *args, **kwargs):
		context = super(AddEmailToCampaignList, self).get_context_data(**kwargs)
		context['title'] = "Newsletter SignUp"
		return context


class EditEmailCampaign(UpdateView):
	form_class = EmailMarketingSignUpForm
	pass





#Banner App
class AddBanner(CreateView):
	pass

