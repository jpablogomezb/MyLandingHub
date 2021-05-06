from django.db import models
from django.utils.translation import ugettext_lazy as _

#Registro de clientes al newsletter
class SignUp(models.Model):
    email = models.EmailField()
    name = models.CharField(_('name'), max_length=240, blank=True, null=True)
    phone_number = models.CharField(_('phone number (cell)'), max_length=60, null=True, blank=True)
    obj_interest_id = models.IntegerField(_('product ID.'), blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
    	if self.active:
    		return "%s %s" %(self.email, 'is subscribed')
    	else:
    		return "%s %s" %(self.email, 'is unsubscribed')