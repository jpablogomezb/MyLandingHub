from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField

from landinghub.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

def landingfile_upload_to(instance, filename):
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(instance.slug, ext)
	return 'landinghub/files/%s/landings/%s' % (instance.owner, filename)

NEWSLETTER_CHOICES = (
        ('NO', 'No'),
		('YNL', _('Yes. Newsletter')),
		# ('YNLD', _('Sí. Newsletter + Cupón Descuento')),
	)

class LandingPage(models.Model):
	owner = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE) # class_instance.model_set.all() #Check CFE Django User model unleashed
	title = models.CharField(_('landing page header'), max_length=100, help_text=_('A catchy title or name for the page.'))
	title_form = models.CharField(_('form title'), max_length=100, help_text=_('Title for the contact form.'), default='DO YOU WANT MORE INFORMATION?')
	slug = models.SlugField(blank=True, null=False, unique=True, max_length=200)
	clock = models.DateTimeField(_('date/time countdown'), help_text=_('Use this field only if you want a countdown to be displayed.'), blank=True, null=True)
	price = MoneyField(_('price to show'), max_digits=19, decimal_places=4, default_currency='USD', blank=True, null=True, help_text=_('Use this field only if you want a price to be displayed.'))
	file = models.FileField(_('file'), upload_to=landingfile_upload_to, editable=True, help_text=_("Upload main file to show in the Landing Page (pdf, ppt, image, video, mp3, etc.)."))
	file_type = models.CharField(max_length=25, null=True)
	newsletter_popup = models.CharField(_('Newsletter subscription pop-up window?'), max_length=4,
	                                  choices=NEWSLETTER_CHOICES,
	                                  default='NO',
									  help_text=_('A pop-up window for visitors to subscribe to your mailing list.'))
	#newsletter_discount = models.IntegerField(_('offer discount coupon of'), default=10, help_text=_('Enter the whole number corresponding to the discount percentage (not including the "%" symbol).'))
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return 'Landing Page: %s' %(self.title)

	def get_absolute_url(self):
	  return reverse("landings:landing-detail", kwargs={"slug":self.slug}) #f"/landings/{self.slug}/"
	
	class Meta:
	    ordering = ["-timestamp", "-updated"]

	# @property
	# def foo(self):
	# 	return self._foo

def landing_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(landing_pre_save_receiver, sender=LandingPage)

