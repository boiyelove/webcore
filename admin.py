from django.contrib import admin
from .models import (
	EmailMarketingSignUp, 
	Banner,
	Contacted_Us,
	Category,
	Tag
	)

# Register your models here.


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'dateUpdated', 'active']
	class Meta:
		model = EmailMarketingSignUp


admin.site.register(Category)
admin.site.register(Tag)	
admin.site.register(Banner)
admin.site.register(Contacted_Us)
admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)





