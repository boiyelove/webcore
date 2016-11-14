from django.conf import settings
from . import models
from django.db.models.signals import post_save
from .utils import code_generator
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=models.EmailVerification)
def emailUnconfirmed(instance, created, **kwargs):
	code_exists = True
	if created:
		emailverificationObj, email_is_created = models.EmailVerification.objects.get_or_create(email = instance.email)
		base, domain = str(instance.email).split("@")
		while code_exists:
			verification_key = code_generator(base)[:10]
			code_exists = models.EmailVerification.filter(slug = verification_key)
			print("ver key is: %s" % verification_key)
		emailverificationObj.slug = verification_key
		emailverificationObj.save()
		emailverificationObj.send_activation_email()

