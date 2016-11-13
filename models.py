from datetime import timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
 


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


#Default Apps Models

class Banner(_TitleSlug):
	desc = models.CharField(max_length = 60)
	btn_link = models.URLField()
	btn_title = models.CharField(max_length = 18)



	# Email Newsletter App
	# NewsLetter SignUp
class EmailMarketingSignUp(_Timestamp):
	email = models.EmailField()
	active = models.BooleanField(default = False)
	subscriptions = models.ManyToManyField('EmailCampaignCategory')

	def __str__(self):
		return self.email


	#Newsletter Verification
class EmailMarketingConfirmed(models.Model):
	subsriber = models.OneToOneField("EmailMarketingSignUp")
	activation_key = models.CharField(max_length=200)
	confirmed = models.BooleanField(default=False)

	def __str__(self):
		return self.confirmed

	def activate_user_email(self):
		activation_url = "%s%s" %(settings.SITE_URL, reverse("marketingactivation_view", args[self.activation_key]))
		context = {
			"activation_key": self.activation_key,
			"activation_url": activation_url,
			"user": self.user.first_name,
		}
		message = render_to_string("newslettersignup/activation_message.txt", context)
		subject = "Activate your email"
		self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.user.email], kwargs)


class EmailCampaignCategory(models.Model):
	title = models.CharField(max_length = 100)
	active = models.BooleanField(default = True)
