from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from mailer import send_mail, send_html_mail
from django import forms
from django.views.generic import (
	CreateView,
	ListView,
)

#from .utils import get_mailchimp_api
from .forms import SignUpForm
from .models import SignUp
from landings.models import LandingPage

#Project Vars
project_logo = settings.PROJECT_LOGO
project_name = settings.PROJECT_NAME
project_domain = settings.PROJECT_DOMAIN
project_product_desc = settings.PRODUCT_DESCRIPTION

class AjaxTemplateMixin(object):

     def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class NewsletterSignupView(SuccessMessageMixin, AjaxTemplateMixin, CreateView):
	#model = SignUp
	template_name = 'signups/newsletter_popup_form.html'
	form_class = SignUpForm
	success_url = reverse_lazy('home')
	#success_message = _("¡Perfecto! Nos comunicamos contigo para ver en cúal curso te interesa aplicar tu beca.")

	def dispatch(self, request, *args, **kwargs):
	    landing = LandingPage.objects.get(id=kwargs['pk'])
	    return super(NewsletterSignupView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(NewsletterSignupView, self).get_context_data(**kwargs)
	    # Add in a QuerySet
	    #landingpage for acitivity get discount
	    landing = LandingPage.objects.get(id=self.kwargs['pk']) 
	    context['landing_id'] = self.kwargs['pk']
	    context['main_header'] = _('Receive exclusive discounts and information about new products and promotions!')
	    context['sub_header'] = _('By subscribing to the Newsletter we will notify you of special discounts and new product launches')
	    form_btn_text = _("I'm interested!")
	    context['btn_submit'] = form_btn_text
	    return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		#email = instance.email
		#fname = instance.first_name
		email = form.cleaned_data.get("email")
		fname = form.cleaned_data['name']
		if not form.cleaned_data['name']:
			fname = '-'
		instance.obj_interest_id = self.kwargs['pk']
		#phone = instance.phone_number
		instance.save()
		# list_id = 'f5a3186ffc'
		# m = get_mailchimp_api()
		# try:
		#     fields={'FNAME':fname}
		#     m.lists.members.create(list_id, { 'email_address': email, 'status': 'subscribed', 'merge_fields':fields, })
		#     try:
		#         SignUp.objects.get_or_create(email=email, first_name=fname)
		#     except Exception as e:
		#         print(e)
		# except Exception as e:
		#     print(e)
		try:
			remitente = settings.EMAIL_PLATFORM
			destinatario = [settings.EMAIL_MAIN]
			sbj = "%s -%s" %(_('New Newsletter subscriber'), project_name)
			url = "https://%s/newsletter/%s/subscriptions/" %(project_domain, str(instance.obj_interest_id))
			msg = "%s" %(_('New subscriber!'))
			msg_bye = "%s -%s" %(_('Best regards'), project_name)
			send_html_mail(sbj, msg, '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td width="10%" align="center" valign="top" style="font-family:Open Sans, Helvetica Neue, Helvetica, Helvetica, Arial, sans-serif; font-size:2px; font-weight:300; color:#294661;">.</td><td width="80%" align="center" valign="top" bgcolor="#f7f7f7"><h2> '+ msg +' </h2><h2 class="text-center">' + fname + '</h2>(<a href=' + url + '>' + url +'</a>)<h3 class="text-center" style="color:#007D8C;"><a href="mailto:'+ email + '">' + email + '</a></strong></h3><p>'+ msg_bye +'<br><br></p></td><td width="10%" align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:2px; color:#ffffff;">.</td></tr></table>', remitente, destinatario, fail_silently=False)
		except Exception as e:
			print('error here 1')
			print(e)
			pass
		try:
			remitente = settings.EMAIL_MAIN
			destinatario = [email]
			sbj = "%s -%s" %(_('Thank you for subscribing'), project_name)
			msg = "%s %s" %(fname, _('Welcome to our Newsletter!'))
			msg2 = "%s" %(_('We will keep you updated with the latest news and updates, and you will receive the exclusive discounts we have for you.'))
			#send_html_mail(sbj, msg, '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td width="10%" align="center" valign="top" style="font-family:Open Sans, Helvetica Neue, Helvetica, Helvetica, Arial, sans-serif; font-size:2px; font-weight:300; color:#294661;">.</td><td width="80%" align="center" valign="top" bgcolor="#f7f7f7"><h2>'+ msg +'</h2><h3>'+ msg2 +'</h3><br><p>' + msg_bye + '</p></td><td width="10%" align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:2px; color:#ffffff;">.</td></tr></table>', remitente, destinatario, fail_silently=False)
			#send_html_mail(sbj, msg, "' '",remitente, destinatario, fail_silently=False )
		except Exception as e:
			print('error here 2')
			print(e)
			pass
		return HttpResponseRedirect(self.success_url)
		#return super(NewsletterSignupView, self).form_valid(form)

class NewsletterSignupListView(LoginRequiredMixin, ListView):
	
	def get_context_data(self, **kwargs):
		context = super(NewsletterSignupListView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = _('Newsletter Subscriptions')
		activity = get_object_or_404(LandingPage, id=self.kwargs['pk'])
		context['landing'] = activity
		return context

	def get_queryset(self):
		#activity_id = self.kwargs['pk']
		activity = get_object_or_404(LandingPage, id=self.kwargs['pk'])
		#activity = .objects.get(id=activity_id)
		queryset = SignUp.objects.filter(obj_interest_id=activity.id).order_by('timestamp')
		#queryset = BookingMessage.objects.filter(booking=activity).order_by('-created')
		return queryset










