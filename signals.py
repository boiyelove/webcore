from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from .models import EmailVerification
from .utils import code_generator


def emailUnconfirmed(sender, instance, created, *args, **kwargs):
	user = instance
	if created:
		user.is_active = False
		emailverificationObj, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
		if email_is_created:
			base, domain = str(user.email).split("@")
			activation_key = code_generator(base)[:10]
			emailverificationObj.slug = activation_key
			emailverificationObj.save()
			emailverificationObj.send_activation_email()



post_save.connect(emailUnconfirmed, sender=EmailVerification)