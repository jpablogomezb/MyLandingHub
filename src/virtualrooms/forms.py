# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from datetime import timedelta, date
from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateWidget, TimeWidget, DateTimeWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML

from .models import VirtualRoomPage, SessionMaterial, AttendeeVroom

class VirtualRoomPageForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(VirtualRoomPageForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False
		self.helper.form_id = 'virtualroompage_form'
		self.helper.layout = Layout(
			Div('name', css_class='col-md-12'),
			Div('facilitator', css_class='col-md-12'),
			HTML("<hr>"),
			Div('date', css_class='col-md-12'),
			Div('hour_from', css_class='col-md-12'),
			Div('clock', css_class='col-md-12'),
			HTML("<hr>"),
			Div('online_room_url', css_class='col-md-12'),
			Div('attendee_info', css_class='col-md-12'),
		)

	class Meta:
		model = VirtualRoomPage
		fields = [
			'name',
			'facilitator',
			'date',
			'hour_from',
			'clock',
			'online_room_url',
			'attendee_info',
		]
		date2=datetime.datetime.now().date() + datetime.timedelta(days=5*30)
		dateOptions = {
			'format': 'yyyy-mm-dd',
			'todayHighlight':True,
			'autoclose': True,
			'pickerPosition': 'bottom-left',
			'startDate': datetime.datetime.now().date().isoformat(),
			'endDate': date2.isoformat()
			}
		timeOptions = {
			'format': 'hh:ii',
			'autoclose': True,
			'minuteStep': 30,
			'pickerPosition': 'bottom-left',
			}


		widgets = {
			'date': DateWidget(options=dateOptions, usel10n=True, bootstrap_version=3),
			'hour_from': TimeWidget(options=timeOptions,  usel10n=True, bootstrap_version=3),
		}


class VirtualRoomMaterialUploaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(VirtualRoomMaterialUploaForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False
		self.helper.form_id = 'material_form'
		self.helper.layout = Layout(
			Div('file', css_class='col-md-12'),
			Div('file_name', css_class='col-md-12'),
			HTML("<br>"),
			Div('file_description', css_class='col-md-12'),
			Div('active', css_class='col-md-12'),
		)

	class Meta:
		model = SessionMaterial
		fields = ['file', 'file_name', 'file_description', 'active']
		widgets = {
		  'file_description': forms.Textarea(attrs={'rows':1}),
		}


class VirtualRoomAttendeeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(VirtualRoomAttendeeForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'required': 'required'})
		self.fields['name'].label = _("Name:")

	class Meta:
		model = AttendeeVroom
		fields = ['name','email']
		widgets = {
			'email': forms.TextInput(attrs={'placeholder': 'abc@email.com'}),
		}
	
		