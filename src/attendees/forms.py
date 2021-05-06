# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Attendee

class AttendeeRegistratioForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'required': 'required'})
		self.fields['name'].label = _("Name:")

	class Meta:
		model = Atteedee
		fields = ['name','email']
		widgets = {
			'email': forms.TextInput(attrs={'placeholder': 'abc@email.com'}),
		}