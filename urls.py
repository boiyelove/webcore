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
	url(r'^subscribe/$', views.AddEmailVerification.as_view(), name = 'verify-email-form'),
	url(r'^subscribe/verify/(?P<verification_key>\w+)/$', views.CheckEmailVerification.as_view(), name = 'verify-email-status'),
	url(r'^subscribe/(?P<subscriber_id>\d+)/add/(?P<campaign_list>\d+)/$', views.UpdateNewsletterSubscription.as_view(), name = 'add-to-campaign'),
	url(r'^unsubscribe/(?P<subscriber_id>\d+)/add/(?P<campaign_list>\d+)/$', views.UpdateNewsletterSubscription.as_view(), name = 'remove-from-campaign'),	#Banner

	#Category

	#Tag

]