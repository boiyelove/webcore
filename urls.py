from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views

#Custom Error Pages Routes
handler400 = views.handler400
handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [

	#Default Pages Routes
	url(r'^$',  views.HomePageView.as_view(), name='home-page'),
	url(r'^aboutus/$', views.AboutUsPageView.as_view(), name = 'about-us'),
	url(r'^contactus/$', views.ContactUsPageView.as_view(), name = 'contact-us'),


	#Default Apps Routes

	#Pages
	
	#Email Campaign
	url(r'^subscribe/$', views.AddEmailToCampaignList.as_view(), name = 'contact-us'),
	url(r'^subscribe/list/$', views.AddEmailToCampaignList.as_view(), name = 'contact-us'),
	url(r'^unsubscribe/$', views.AddEmailToCampaignList.as_view(), name = 'contact-us'),

	#Banner

	#Category

	#Tag

]