from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.conf import settings
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView
from projectflow.models import Project, Task
from teamflow.models import Team, TeamInvite
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import (ContactForm, 
					EmailMarketingSignUpForm,
					CategoryForm,
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


class AddHeader:
	page_header = None
	page_tagline = settings.SITE_TAGLINE
	page_title = ''

	def get_context_data(self, *args, **kwargs):
		context = super(AddHeader, self).get_context_data(*args, **kwargs)
		context['page_header'] = self.page_header
		context['page_tagline'] = self.page_tagline
		context['page_title'] = self.page_title 
		return context


#DUmmy Template Views
class WebcoreTemplateView(TemplateView):
	apname = "Webcore"

	def get_context_data(self, *args, **kwargs):
		context = super(WebcoreTemplateView, self).get_context_data(*args, **kwargs)
		context.update({'app_name': self.apname,
			'page_title' : 'WorkFlow',})
		return context


#Default Website Pages
	#templates at _dwp/
class HomePageView(TemplateView):

	def get_template_names(self, *args, **kwargs):
		if self.request.user.is_authenticated():
			self.template_name = 'teamflow/workdashboard.html'
		else:
			self.template_name = "webcore/_dwp/wpc_home.html"
		return [self.template_name]

	def get_context_data(self, *args, **kwargs):
		context = super(HomePageView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated():
			context.update({
			"project_list": Project.objects.all(),
			"task_list": Task.objects.all(),
			"team_list": Team.objects.all(),
			"invite_list": TeamInvite.objects.all(), 
			"header": "WorkDash"
			})
		else:
			context.update({
				'page_title' : 'Team WorkFlow',
				"header": "Join WorkFlow"
				})
		return context




class AboutUsPageView(WebcoreTemplateView):
	apname = "About Us"
	template_name = "webcore/_dwp/wpc_aboutus.html"


class ContactUsPageView(CreateView):
	form_class = ContactForm
	template_name = "accounts/form.html"
	success_url = reverse_lazy('webcore:home-page')

	def get_context_data(self, *args, **kwargs):
		context = super(ContactUsPageView, self).get_context_data(*args, **kwargs)
		context.update({'page_title' : 'Contact Our Team',
		'form_title': 'Contact Revenupa Team',
		"form_action": reverse_lazy('webcore:contact-us'),
		"form_method": "post",
		"form_value": "Send this Message",
		})
		return context




class PageView(TemplateView):
	template_name = "webcore/_dwp/wbc_page.html"






#Default Webste Apps
	#templates at _dwa/

#Category App
class CategoryView:
	form_class = CategoryForm
	success_url = reverse_lazy("webcore/_dwa/category-detail")
	
class CategoryCreateView(CategoryView, CreateView):

	def get_context_data(*args, **kwargs):
		context = super(CreateCategory, self).get_context_data(**kwargs)
		context['head_title'] = "Create New Category"
		context["page_title"] = "Create New category"
		context["btn_title"] = "Create Category"
		return context

class CategoryUpdateView(CategoryView, UpdateView):

	def get_context_data(*args, **kwargs):
		context = super(CreateCategory, self).get_context_data(**kwargs)
		context['head_title'] = "Update Category"
		context["page_title"] = "Update category"
		context["btn_title"] = "Update Category"
		return context


class CategoryDeleteView(DeleteView):
	model = Category
	success_url = reverse_lazy("webcore/_dwa/category-list")

class CategoryListView(ListView):
	model = Category
	template_name = "webcore/_dwa/category_list.html"

class CategoryDetailView(DetailView):
	model = Category
	template_name = "webcore/_dwa/category_detail.html"



#Pages App
class AddWebsitePage(CreateView):
	pass


# class AjaxMixin(object):
# 	def  get(self, request, *args, **kwargs):
# 		data = {}
# 		return render_to_response(self.template_name, data, context_instance = RequestContext(request))

# 	@method_decorator(ajax_rquest)
# 	def dispatch(self, *args, **kwargs):
# 		return super(AjaxMixin, self).dispatch(*
# 			args, **kwargs)


class AjaxableResponseMixin(object):
	def form_invalid(self, form):
		response = super(AjaxableResponseMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):
		response = super(AjaxableResponseMixin, self).form_valid(form)
		if self.request.is_ajax():
			data = {'pk': self.object.pk}
			return JsonResponse(data)
		else:
			return response







#Newsletter App
# webcore/_dwa/Newsletter

class UpdateNewsletterSubscription(UpdateView):
	form_class= EmailMarketingSignUpForm
	template_name = "webcore/form.html"
	

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateNewsletterSubscription, self).get_context_data(*args, **kwargs)
		context['head_title'] = "Update Subscription"
		context["page_title"] = "Update Subscription"
		context["btn_title"] = "Update Subscription"
		return context

#Banner App
class AddBanner(CreateView):
	pass


