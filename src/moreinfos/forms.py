# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import MoreInfo

class MoreInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MoreInfoForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'required': 'required'})
        self.fields['email'].widget.attrs.update({'required': 'required'})
        self.fields['phone_number'].widget.attrs.update({'required': 'required'})

    class Meta:
    	model = MoreInfo
    	fields = ('user','name','email', 'phone_number', 'obj_interest_id')
    	#fields = '__all__'
    	#exclude = ['user']
    	#widgets = {'user': forms.HiddenInput()}
    	widgets = {
    		#'subject': forms.TextInput(attrs={'placeholder': 'Información, Lugares, Ventas, Sugerencia, etc. '}),
    		#'message': forms.Textarea(attrs={'rows':8, 'placeholder': 'Escribe aquí tu mensaje.'}),
            'obj_interest_id': forms.HiddenInput(),
    		'email': forms.TextInput(attrs={'placeholder': 'nombre@email.com'}),
    		#'phone_number': forms.TextInput(attrs={'placeholder': '+520000000000'}),
    		#'people_number': forms.Select(choices=NUMBERS),
    	}