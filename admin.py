from django.contrib import admin
from .models import (
	EmailVerification,
	EmailMarketingSignUp, 
	Banner,
	Contacted_Us
	)

# Register your models here.


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'updated_on', 'active']
	class Meta:
		model = EmailMarketingSignUp
		
admin.site.register(Banner)
admin.site.register(Contacted_Us)
admin.site.register(EmailVerification)
admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)





