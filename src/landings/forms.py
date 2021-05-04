# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from datetime import timedelta, date
from django import forms
from datetimewidget.widgets import DateTimeWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from .models import LandingPage

class LandingPageForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(LandingPageForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_tag = False
		self.helper.form_id = 'landing_form'
		self.helper.layout = Layout(
			Div('title', css_class='col-md-12'),
			HTML("<hr>"),
			Div('file', css_class='col-md-12'),
			HTML("<hr>"),
			Div('clock', css_class='col-md-12'),
			Div('price', css_class='col-md-12'),
			HTML("<hr>"),
			Div('title_form', css_class='col-md-12'),
			HTML("<hr>"),
			Div('newsletter_popup', css_class='col-md-12'),
			# Div(
			# 	Div('newsletter_discount', css_class='col-md-12'),
			# 	css_id='newsletter_discount',
			# ),
			HTML("<br>"),
		)

	class Meta:
		model = LandingPage
		fields = [
			'title',
			'file',
			'clock',
			'price',
			'title_form',
			'newsletter_popup',
			#'newsletter_discount'
		]
		date2=datetime.datetime.now().date() + datetime.timedelta(days=5*30)
		dateTimeOptions = {
			'format': 'yyyy-mm-dd',
			'todayHighlight':True,
			'autoclose': True,
			'pickerPosition': 'bottom-left',
			'startDate': datetime.datetime.now().date().isoformat(),
			'endDate': date2.isoformat(),
			'format': 'hh:ii',
			'autoclose': True,
			'minuteStep': 15,
			'pickerPosition': 'bottom-left',
			}
		widgets = {
			#'keywords': autocomplete.TaggingSelect2('tags-autocomplete'),
			'clock': DateTimeWidget(options = dateTimeOptions, usel10n = True, bootstrap_version=3),
		}

	
		