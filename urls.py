from django.conf.urls import url, handler400, handler403, handler404, handler500
from . import views

#Custom Error Pages Routes
handler400 = views.handler400
handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [

	#Default Pages Routes
	url(r'^about/$', views.AboutUsPageView.as_view(), name = 'aboutus'),
	url(r'^contact/$', views.ContactUsPageView.as_view(), name = 'contactus'),
	url(r'^$',  views.HomePageView.as_view(), name='homepage'),

	#Default Apps Routes
	url(r'^newslettersignup/$', views.newsletter_signup , name = 'newslettersignup'),

]