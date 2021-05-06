import datetime
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from landinghub.utils import unique_slug_generator
from attendees.models import Attendee

User = settings.AUTH_USER_MODEL

# Create your models here.
class VirtualRoomPage(models.Model):
	owner = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE) # class_instance.model_set.all() #Check CFE Django User model unleashed
	name = models.CharField(_('activity / event name'), max_length=150, help_text=_('Name or title of the activity, event, or session.'))
	facilitator = models.CharField(_('facilitator / exhibitor'), max_length=150, blank=True, help_text=_('Name of Facilitator/Exhibitor (you can leave blank).'))
	slug = models.SlugField(blank=True, null=False, unique=True, max_length=200)
	date = models.DateField(_('date'), help_text=_('Scheduled date.'), null=False, blank=False)
	hour_from = models.TimeField(_('start time'), help_text=_('Time at which the session is scheduled to begin.'), null=False, blank=False)
	clock = models.BooleanField(verbose_name=_('date/time countdown?'), help_text=_('Countdown to the start of the activity.'), default=True)
	datetime_from = models.DateTimeField(null=True, blank=True)
	online_room_url = models.URLField(_('online room link'), max_length=250, null=False, blank=False, help_text=_('Web link (URL) to the virtual room where the online activity takes place.'))
	attendee_info = models.BooleanField(_('Attendee info?'), help_text=_('Requests the e-mail address and name of the attendee to access the page.'), default=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return 'Virtual Room Page: %s' %(self.name)

	def get_absolute_url(self):
	  return reverse("virtualrooms:virtualroom-detail", kwargs={"slug":self.slug})

	class Meta:
	    ordering = ["-timestamp", "-updated"]

def materialfile_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}-{}.{}'.format(instance.file_name, uuid4().hex, ext)
    return 'landinghub/files/%s/virtualrooms/%s/materials/%s' % (instance.session.owner, instance.session.id, filename)

class SessionMaterial(models.Model):
	session = models.ForeignKey(VirtualRoomPage, on_delete=models.CASCADE, related_name='materials')
	file = models.FileField(_('file'), upload_to=materialfile_upload_to, editable=True, help_text=_("Upload the support material file."))
	file_type = models.CharField(max_length=25, blank=True)
	file_name = models.CharField(_('material (file) name'), max_length=30, blank=True)
	file_description = models.TextField(_('material (file) description'), max_length=80, help_text=_('Describe or explain what the support material consists of (you can leave blank).'), blank=True)
	active = models.BooleanField(verbose_name=_('active material?'), default=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return 'Material: %s' %(self.file_name)

	class Meta:
	    ordering = ["-timestamp", "-updated"]

class AttendeeVroom(Attendee):
	session = models.ForeignKey(VirtualRoomPage, null=True, on_delete=models.SET_NULL, related_name='attendees')

	def __str__(self):
		if self.name:
			return  "%s -%s" %(self.email, self.name)
		else:
			return self.email


def virtualroompage_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	if instance.clock == True:
		try:
		    instance.datetime_from = datetime.datetime.combine(instance.date, instance.hour_from)
		except Exception as e:
			instance.clock = False

pre_save.connect(virtualroompage_pre_save_receiver, sender=VirtualRoomPage)
