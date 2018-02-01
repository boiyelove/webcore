from datetime import timedelta
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify
 


def get_sentinel_user():
	return get_user_model.objects.get_or_create(username="deleted")[0]

def get_sentinel_category():
	return Category.objects.get_or_create(title="Other")

def wait_for(t=+1):
	return timezone.now() - timedelta(hours=t)

def validate_only_one_instance(obj):
	model = obj.__class__
	if (model.objects.count() > 0 and obj.id != model.objects.get().id):
		raise ValidationError("Can only create on instance of %s" % model.__name__)


class AuthorDraftManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(AuthorDraftManager, self).filter(active=True).filter(draft=False).filter(datePublished__lte=timezone.now())

class TimestampedModel(models.Model):
	dateCreated = models.DateTimeField(auto_now_add=True)
	dateUpdated = models.DateTimeField(auto_now = True)
	datePublished = models.DateTimeField(null=True, blank=True)

	class Meta:
		abstract = True


class ABC_TitleSlug(TimestampedModel):
	title = models.CharField(max_length = 80, default="Sample Title")
	slug = models.SlugField(unique = True, default="sample_title")

	class Meta:
		abstract = True

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		obj = super(ABC_TitleSlug, self).__class__
		#if the object has not been saved
		#if object has no slug or has default slug set
		#if the object has already been saved
		#and the title is diffent from the slug
		#set the slug by the title
		if (self.pk and (not self.slug or (self.slug == "sample_title"))) or (self.pk and (self.title != self.slug)):
			slugset = False
			count = 0
			while not slugset:	
				try:
					#try to check if an object with the slug exists
					obj.objects.get(slug = self.title)
					#if it exists, increment count
					count += 1
				#if it does not exist, set it with the new number
				except obj.DoesNotExist:
					slug = slugify(self.title + '_{0}'.format(count))
					self.slug = slug
					slugset  = True
		super(ABC_TitleSlug, self).save(*args, **kwargs)



class ABC_AuthorDraft(ABC_TitleSlug):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET(get_sentinel_user), default=1)
	draft = models.BooleanField(default = False)
	active = models.BooleanField(default = True)

	objects = AuthorDraftManager()

	class Meta:
		abstract = True

	def clean(self):
		if self.draft == True and self.datePublished is not None:
			raise ValidationError(_('Draft entries should not have a publication date.'))
		if not self.draft and not self.datePublished:
			self.datePublished = timezone.now()


class Tag(ABC_AuthorDraft):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET(get_sentinel_user), default=1, related_name="tag_creator")
	
	def get_absolute_url(self):
			return reverse_lazy('webcore:webcore-tag-view', kwargs={'slug': self.slug})


class Category(ABC_AuthorDraft):
	parent = models.ForeignKey('self', null=True, blank=True, related_name = "parent_category")
	description = models.CharField(max_length = 60, null=True, blank = True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET(get_sentinel_user), default=1, related_name="category_creator")
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
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
		return reverse_lazy('webcore:webcore-category', kwargs={'slug': self.slug})

class ABC_OnePageModel(ABC_AuthorDraft):
	content = models.TextField(default="Sample Content")

	class Meta:
		abstract = True

	def clean(self):
		validate_only_one_instance(self)



#Default Pages Models
class About_website(ABC_OnePageModel):
	logo = models.ImageField(upload_to="website_logo", null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	tel = models.CharField(max_length = 50, null=True, blank=True)


class Contacted_Us(TimestampedModel):
	subject = models.CharField(max_length = 30, default="Sample Subject")
	name = models.CharField(max_length=30)
	email = models.EmailField(default="example@domain.ext")
	content = models.TextField(default="Sample Message Content")


	def clean(self):
		validate_only_one_instance(self)


	def __str__(self):
		return( '%s - %s', self.email, self.subject)



class WebsitePage(ABC_OnePageModel):
	link = models.URLField(null=True, blank=True)
	content = models.TextField(default="Sample Web Page Content")


class Template(ABC_AuthorDraft):
	pass





#Default Apps Models





# NewsLetter SignUp
class EmailMarketingSignUp(TimestampedModel):
	name = models.CharField(max_length = 50, null=True, blank=True)
	email = models.EmailField()
	active = models.BooleanField(default = False)
	subscriptions = models.ManyToManyField('EmailCampaignCategory')

	def __str__(self):
		return self.email

class EmailCampaignCategory(ABC_TitleSlug):
	title = models.CharField(max_length = 100)
	active = models.BooleanField(default = True)
	parent = models.ForeignKey('self', null=True, blank=True)

	def __str__(self):
		return self.title


#Web Profile App
class WebProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='webcore_profile')
    photo = models.ImageField(upload_to='webcore/profile_photo', null=True)
 
    def __str__(self):
        return "{}'s profile".format(self.user.username)



#Banner
class Banner(ABC_TitleSlug):
	desc = models.CharField(max_length = 60)
	btn_link = models.URLField()
	btn_title = models.CharField(max_length = 18)

class VisitedUrl(TimestampedModel):
	url = models.URLField()
	views = models.PositiveIntegerField(default = 0)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

	def __str__(self):
		return '%s' % self.url