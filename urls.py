from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views

#Custom Error Pages Routes
handler400 = views.handler400
handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500

app_name = 'webcore'
urlpatterns = [

	#Default Pages Routes
	url(r'^$',  views.HomePageView.as_view(), name='home-page'),
	url(r'^aboutus/$', views.AboutUsPageView.as_view(), name = 'about-us'),
	url(r'^contactus/$', views.ContactUsPageView.as_view(), name = 'contact-us'),
	
	
	# #Email Campaign
	# url(r'^subscribe/$', views.AddEmailVerification.as_view(), name = 'verify-email-form'),
	# url(r'^subscribe/verify/(?P<verification_key>[\w-]+)/$', views.CheckEmailVerification.as_view(), name = 'verify-email-status'),
	# url(r'^subscribe/(?P<subscriber_id>\d+)/add/(?P<campaign_list>\d+)/$', views.UpdateNewsletterSubscription.as_view(), name = 'add-to-campaign'),
	# url(r'^unsubscribe/(?P<subscriber_id>\d+)/add/(?P<campaign_list>\d+)/$', views.UpdateNewsletterSubscription.as_view(), name = 'remove-from-campaign'),	#Banner
	
	
	#Category
	url(r'^category/$', views.CategoryListView.as_view(), name="webcore-category-List"),
	url(r'^category/add/$', views.CategoryCreateView.as_view(), name="webcore-category-create"),
	url(r'^category/(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name="webcore-category-detail"),
	url(r'^category/(?P<slug>[\w-]+)/edit/$', views.CategoryUpdateView.as_view(), name="webcore-category-edit"),
	url(r'^category/(?P<slug>[\w-]+)/delete/$', views.CategoryDeleteView.as_view(), name="webcore-category-delete"),
	url(r'^categpry/(?P<pk>[\d]+)/$', views.CategoryDetailView.as_view(), name ="webcore-category-pk"),	

	#Pages
	# url(r'^create_page/$', views.PageCreateView.as_view(), name="webcore-page-create"),
	# url(r'^(?P<slug>[\w-]+)/$', views.PageDetailView.as_view(), name="webcore-page-detail"),
	# url(r'^(?P<slug>[\w-]+)/edit/$', views.PageUpdateView.as_view(), name="webcore-page-edit"),
	# url(r'^(?P<slug>[\w-]+)/delete/$', views.PageDeleteView.as_view(), name="webcore-page-delete"),
	# url(r'^(?P<pk>[\d]+)/$', views.PageDetailView.as_view(), name ="webcore-page-pk"),



	#Tag

#Default Apps Routes

]