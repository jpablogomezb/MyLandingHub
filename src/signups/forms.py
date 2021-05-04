# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import SignUp

class SignUpForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
	    #Aquí puedo hacer modificaciones al modelo y la presentación
	    #del formulario
		self.fields['email'].widget.attrs.update({'required': 'required'})
		#self.fields['email'].label = _("Correo electrónico:")
		self.fields['name'].label = _("Name:")

	class Meta:
		model = SignUp
		fields = ['name','email', 'obj_interest_id']
		widgets = {
			'obj_interest_id': forms.HiddenInput(),
			'email': forms.TextInput(attrs={'placeholder': 'abc@email.com'}),
		}