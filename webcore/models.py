from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
 

 def get_sentinnel_user():
	return get_user_model.objects.get_or_create(username="deleted")[0]

class Timestamp(models.Model):
	created_on = models.DateTimeField(auto_now = True)
	updated_on = models.DateTimeField(auto_now_add = True)
	published_date = models.DateTimeField(blank=True, null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET(get_sentinnel_user))
	draft = models.BooleanField(default = False)
	class Meta:
		abstract = True

	def publish(self):
		self.published_date = timezone.now()
		self.save()

class Musthave(Timestamp):
	title = models.CharField(max_length = 80, unique=True)
	slug = models.SlugField(unique = True)
	class Meta:
		abstract = True

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
			super(Category, self).save(*args, **kwargs)


class Tag(Musthave):

	def get_absolute_url(self):
			return reverse_lazy('blog:blog_tag_view', kwargs={'slug': self.slug})


class Category(Musthave):
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
		return reverse_lazy('blog:blog_category', kwargs={'slug': self.slug})

class OnePageModel(Musthave):

	def clean(self):
		validate_only_one_instance(self)



#Default Pages Models
class About_website(OnePageModel):
	logo = models.ImageField(upload_to="website_logo")
	about = models.TextField()
	address = models.CharField(max_length=100)
	tel = models.CharField(max_length = 50)
	email = models.EmailField()

class Contact(OnePageModel):
	name = models.CharField(max_length = 30, null=True)
	email =models.EmailField()
	subject = models.CharField(max_length = 30)
	content = models.TextField()
	created = models.DateTimeField(auto_now = True, auto_now_add=False)
	updated = models.DateTimeField(auto_now = False, auto_now_add=True)

	def __str__(self):
		return( '%s - %s', self.email, self.subject)



class WebsitePage(models.Model):
	title = models.CharField(max_length = 100)
	slug = models.SlugField(unique = True)
	link = models.URLField()
	content = models.TextField()



class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to='profile_photo', null=True)
 
    def __str__(self):
        return "{}'s profile".format(self.user.username)
 
    class Meta:
        db_table = 'user_profile'
 
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


#Default Apps Models

class Banner(Musthave):
	desc = models.CharField(max_length = 60)
	btn_link = models.URLField()
	btn_title = models.CharField(max_length = 18)


class EmailMarketingSignUp(Timestamp):
	email = models.EmailField()
	active = models.BooleanField(default = False)

	def __str__(self):
		return self.email


class EmailMarketingConfirmed(TImestamp):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
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




def validate_only_one_instance(obj):
	model = obj.__class__
	if (model.objects.count() > 0 and obj.id != model.objects.get().id):
		raise ValidationError("Can only create on instance of %s" % model.__name__)