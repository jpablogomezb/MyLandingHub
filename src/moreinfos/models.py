from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = settings.AUTH_USER_MODEL

#Personas solicitando más información
class MoreInfo(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=120, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(_('phone number (cell)'), max_length=60, null=True, blank=True)
    obj_interest_id = models.IntegerField(_('product ID.'), blank=True, null=True)
    #organization = models.CharField(_('organization'), max_length=120, null=True, blank=True)
    #people_number = models.IntegerField(_('number of persons'), default=1, validators=[MinValueValidator(1)])
    #subject = models.CharField(_('subject'), max_length=120, null=True, blank=True)
    #message = models.TextField(_('message'), max_length=4000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
    	if self.name:
    		return "%s %s %s" %(self.name, "is interested in product ID.:", self.obj_interest_id)
    	else:
    		return "%s %s" %(self.email, "is interested in product ID.:", self.obj_interest_id)