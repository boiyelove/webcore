from datetime import timedelta
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
 


def get_sentinel_user():
	return get_user_model.objects.get_or_create(username="deleted")[0]

def get_sentinel_category():
	return Category.objects.get_or_create(title="Other")

def get_waittime(t=+1):
	return timezone.now() - timedelta(hours=t)

def validate_only_one_instance(obj):
	model = obj.__class__
	if (model.objects.count() > 0 and obj.id != model.objects.get().id):
		raise ValidationError("Can only create on instance of %s" % model.__name__)

class _Timestamp(models.Model):
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now = True)
	published_on = models.DateTimeField(null=True, blank=True)

	class Meta:
		abstract = True

	def publish(self):
		self.published_date = timezone.now()
		self.save()


class _TitleSlug(_Timestamp):
	title = models.CharField(max_length = 80, unique=True, default="Sample Title")
	slug = models.SlugField(unique = True, default="sample_title")
	class Meta:
		abstract = True

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
			super(Category, self).save(*args, **kwargs)

class _AuthorDraft(_TitleSlug):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET(get_sentinel_user), default=1)
	draft = models.BooleanField(default = False)
	active = models.BooleanField(default = True)

	class Meta:
		abstract = True

	def clean(self):
		if self.draft == True and self.published_on is not None:
			raise ValidationError(_('Draft entries may not have a publication date.'))
		if self.draft == 'published' and self.published_on is None:
			self.self.published_on = get_waittime()


class Tag(_AuthorDraft):

	def get_absolute_url(self):
			return reverse_lazy('webcore:webcore_tag_view', kwargs={'slug': self.slug})


class Category(_AuthorDraft):
	parent = models.ForeignKey('self', null=True, blank=True)
	description = models.CharField(max_length = 60, null=True, blank = True)

	class Meta:
		verbose_name_plural = "categories"

	def get_subcategories(self):
		return self.objects.filter(
			parent_category__id=target_category.id)

	def get_parent(self):
		if self.parent is not None:
			return self.parent
		else:
			return None

	def get_absolute_url(self):
		return reverse_lazy('webcore:webcore_category', kwargs={'slug': self.slug})

class _OnePageModel(_AuthorDraft):
	content = models.TextField(default="Sample Content")

	class Meta:
		abstract = True

	def clean(self):
		validate_only_one_instance(self)



#Default Pages Models
class About_website(_OnePageModel):
	logo = models.ImageField(upload_to="website_logo", null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	tel = models.CharField(max_length = 50, null=True, blank=True)


class Contacted_Us(models.Model):
	subject = models.CharField(max_length = 30, default="Sample Subject")
	email = models.EmailField(default="example@domain.ext")
	content = models.TextField(default="Sample Message Content")


	def clean(self):
		validate_only_one_instance(self)


	def __str__(self):
		return( '%s - %s', self.email, self.subject)



class WebsitePage(_OnePageModel):
	link = models.URLField(null=True, blank=True)
	content = models.TextField(default="Sample Web Page Content")






#Default Apps Models



#Email Verification
class EmailVerification(_Timestamp):
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	email = models.EmailField(default = "example@domain.ext", unique=True)
	slug = models.SlugField(null = True)
	confirmed = models.BooleanField(default=False)
	action = models.CharField(max_length =15, default="NEWSLETTER")

	def __str__(self):
		return self.confirmed

	def send_activation_email(self):
		print("sending email")
		verification_url = "%s%s" %(settings.SITE_URL, reverse_lazy("verify-email-status", kwargs={"verification_key":self.slug}))
		context = {
			"website": settings.SITE_URL,
			"verification_url": verification_url,
			"user": self.first_name,
		}
		message = render_to_string("webcore/_dwa/newsletter/verification_message.txt", context)
		subject = "Activate your email"
		self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
		print("sent email")

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], kwargs)

	def get_action(self):
		url_action = "/"
		if self.action == "USER":
			user = get_object_or_404(User, email=self.email)
			user.active = True
			user.save()
			
		elif self.action == "NEWSLETTER":
			objEmailMarketingSignUp, just_created = EmailMarketingSignUp.objects.get_or_create(email = self.email)
			objEmailMarketingSignUp.active=True
			objEmailMarketingSignUp.save()
		return url_action


# NewsLetter SignUp
class EmailMarketingSignUp(_Timestamp):
	name = models.CharField(max_length = 50, null=True, blank=True)
	email = models.EmailField()
	active = models.BooleanField(default = False)
	subscriptions = models.ManyToManyField('EmailCampaignCategory')

	def __str__(self):
		return self.email

class EmailCampaignCategory(_TitleSlug):
	title = models.CharField(max_length = 100)
	active = models.BooleanField(default = True)
	parent = models.ForeignKey('self', null=True, blank=True)

	def __str__(self):
		return self.title


#Web Profile App
class WebProfile(models.Model):
    user = models.OneToOneField(User, related_name='webcore_profile')
    photo = models.ImageField(upload_to='webcore/profile_photo', null=True)
 
    def __str__(self):
        return "{}'s profile".format(self.user.username)
 
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])



#Banner
class Banner(_TitleSlug):
	desc = models.CharField(max_length = 60)
	btn_link = models.URLField()
	btn_title = models.CharField(max_length = 18)