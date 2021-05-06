from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = settings.AUTH_USER_MODEL

class Attendee(models.Model):
	user = models.ForeignKey(User, verbose_name=_('user'), null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(_('name'), max_length=120, null=True, blank=True)
	email = models.EmailField()
	phone_number = models.CharField(_('phone number (cell)'), max_length=60, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		if self.name:
			return  "%s -%s" %(self.email, self.name)
		else:
			return self.email

	class Meta:
		verbose_name = "Attendee"
		verbose_name_plural = "Attendees"