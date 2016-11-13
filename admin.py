from django.contrib import admin
from .models import (
	EmailMarketingConfirmed,
	EmailMarketingSignUp, 
	Banner, 
	Contact
	)

# Register your models here.


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'timestamp', 'active']
	class Meta:
		model = EmailMarketingSignUp
		
admin.site.register(Banner)
admin.site.register(Contact)
admin.site.register(EmailMarketingConfirmed)
admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)





