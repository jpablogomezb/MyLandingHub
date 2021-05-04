from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from mailer import send_mail, send_html_mail
from django import forms

from landinghub.utils import check_in_memory_mime
from moreinfos.forms import MoreInfoForm

from django.views.generic import (
	CreateView,
	DetailView,
	ListView,
	UpdateView,
	DeleteView,
)
from django.views.generic.edit import FormMixin

from .models import LandingPage
from .forms import LandingPageForm


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

#class-based views
class LandingPageCreateView(LoginRequiredMixin, CreateView):
	template_name = 'landings/landingpage_create.html'
	form_class = LandingPageForm

	def dispatch(self, request, *args, **kwargs):
		return super(LandingPageCreateView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(LandingPageCreateView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = "%s %s" %(_('Create'), 'Landing Page')
		context['title_action'] = "%s %s" %(_('Create'), 'Landing Page')
		return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		#print(check_in_memory_mime(self.request.FILES['file']))
		actual_user = User.objects.get(username=self.request.user)
		instance.owner = actual_user
		try:
			instance.file_type = str(check_in_memory_mime(self.request.FILES['file']))
			if instance.file_type.find('word') != -1:
				instance.file_type = 'doc'
			elif instance.file_type.find('spreadsheet') != -1:
				instance.file_type = 'xls'
			elif instance.file_type.find('powerpoint') != -1:
				instance.file_type = 'ppt'
			else:
				pass
		except Exception as e:
		    print(e)
		instance.save()
		return super(LandingPageCreateView, self).form_valid(form)


class LandingPageUpdateView(LoginRequiredMixin, UpdateView):
	model = LandingPage
	form_class = LandingPageForm
	template_name = 'landings/landingpage_create.html'
	queryset = LandingPage.objects.all()
	#success_url ="/"
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		landing = get_object_or_404(LandingPage, id=self.kwargs['pk'])
		if self.request.user == landing.owner:
			pass
		else:
			return reverse('landings:landing-list')
		return super(LandingPageUpdateView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LandingPageUpdateView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		landing = get_object_or_404(LandingPage, id=self.kwargs['pk'])
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['landing'] = landing
		context['title'] = "%s %s" %(_('Update'), 'Landing Page')
		context['title_action'] = "%s %s" %(_('Update'), 'Landing Page')
		return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		#print(check_in_memory_mime(self.request.FILES['file']))
		actual_user = User.objects.get(username=self.request.user)
		instance.owner = actual_user
		try:
			instance.file_type = str(check_in_memory_mime(self.request.FILES['file']))
			if instance.file_type.find('word') != -1:
				instance.file_type = 'doc'
			elif instance.file_type.find('spreadsheet') != -1:
				instance.file_type = 'xls'
			elif instance.file_type.find('powerpoint') != -1:
				instance.file_type = 'ppt'
			else:
				pass
		except Exception as e:
		    print(e)
		instance.save()
		return super(LandingPageUpdateView, self).form_valid(form)

	# def form_valid(self, form):
	# 	print(form.cleaned_data)
	# 	return super().form_valid(form)

class LandingPageDeleteView(LoginRequiredMixin, DeleteView,):
	queryset = LandingPage.objects.all()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LandingPageDeleteView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = "%s %s" %(_('Delete'), 'Landing Page')
		return context

	def get_success_url(self):
		return reverse('landings:landing-list')

class LandingPageListView(LoginRequiredMixin, ListView):
	#template_name = ''
	#queryset = LandingPage.objects.all()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LandingPageListView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = 'Landing Pages'

		return context

	def get_queryset(self):
		#activity_id = self.kwargs['pk']
		#activity = .objects.get(id=activity_id)
		queryset = LandingPage.objects.filter(owner=self.request.user).order_by('title')
		#queryset = BookingMessage.objects.filter(booking=activity).order_by('-created')
		return queryset


def landing_page(request, slug):
	context = {}
	landing = get_object_or_404(LandingPage, slug=slug)
	if landing.file_type == 'application/pdf' or landing.file_type.split("/")[0] == 'text' or landing.file_type == 'doc' or landing.file_type == 'xls' or landing.file_type == 'ppt':
		render_file = 'iframe'
	elif landing.file_type.split("/")[0] == 'image':
	    render_file = 'image'
	elif landing.file_type.split("/")[0] == 'video':
	    render_file = 'video'
	elif landing.file_type.split("/")[0] == 'audio':
	    render_file = 'audio'
	else:
	    render_file = 'application/x-empty'

	title = _("%s") %(landing.title)
	btn_submit = _('Yes')
	form = MoreInfoForm(request.POST or None)
	confirm_message = ""
	form.fields['user'].widget.attrs['disabled'] = True

	if not request.user.is_authenticated:
		form.fields['user'].widget = forms.HiddenInput()
		#form.fields['user'].widget.attrs['enabled'] = False
	else:
		form.fields['user'].initial = request.user
		form.fields['name'].initial = request.user.first_name + ' ' + request.user.last_name
		form.fields['email'].initial = request.user.email

	if form.is_valid():
		new_message = form.save(commit=False)
		name = str(form.cleaned_data['name'])
		if not form.cleaned_data['name']:
			name = '-'
		phone = str(form.cleaned_data['phone_number'])
		if not form.cleaned_data['phone_number']:
		    phone = '-'
		mail = form.cleaned_data['email']
		landing = get_object_or_404(LandingPage, slug=slug)
		sbj = "%s %s" %(_('Interested in'), str(landing.title))
		remitente = settings.EMAIL_PLATFORM
		destinatario = [settings.EMAIL_MAIN]
		new_message.obj_interest_id = landing.id

		msg = "%s" %(_('Information Request'))
		msg_bye = "%s -%s" %(_('Best regards'), project_name)
		if request.user.is_authenticated:
			try:
			    send_html_mail(sbj, msg, '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td width="10%" align="center" valign="top" style="font-family:Open Sans, Helvetica Neue, Helvetica, Helvetica, Arial, sans-serif; font-size:2px; font-weight:300; color:#294661;">.</td><td width="80%" align="center" valign="top" bgcolor="#f7f7f7"><h2>' + msg + '</h2><h2 class="text-center">' + name + ' (User: '+ str(request.user) +')</h2><h3 class="text-center" style="color:#007D8C;"><a href="mailto:'+ mail + '">' + mail + '</a></strong></h3><h3 class="text-center" style="color:#007D8C;"><a href="tel:'+ phone + '">tel. ' + phone + '</a></strong></h3><hr><h3 class="text-center">Landing Page: ' + str(landing.title) + '</h3><hr><p>' + msg_bye +'</p></td><td width="10%" align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:2px; color:#ffffff;">.</td></tr></table>', remitente, destinatario, fail_silently=False)
			except Exception as e:
				print('error 1')
				print(e)
			new_message.user = request.user
		else:
			try:
				send = send_html_mail(sbj, msg, '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td width="10%" align="center" valign="top" style="font-family:Open Sans, Helvetica Neue, Helvetica, Helvetica, Arial, sans-serif; font-size:2px; font-weight:300; color:#294661;">.</td><td width="80%" align="center" valign="top" bgcolor="#f7f7f7"><h2>' + msg + '</h2><h2 class="text-center">' + name + '</h2><h3 class="text-center" style="color:#007D8C;"><a href="mailto:'+ mail + '">' + mail + '</a></strong></h3><h3 class="text-center" style="color:#007D8C;"><a href="tel:'+ phone + '">tel. ' + phone + '</a></strong></h3><hr><h3 class="text-center">Landing Page: ' + str(landing.title) + '</h3><hr><p>' + msg_bye +'</p></td><td width="10%" align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:2px; color:#ffffff;">.</td></tr></table>', remitente, destinatario, fail_silently=False)
			except Exception as e:
				print('error 2')
				print(e)

		new_message.save()
		confirm_message = format_html(_("Thank you for your interest!<br><b>We will contact you as soon as possible</b>"))
		form  = None

	context = {
	    "object": landing,
	    "file": render_file,
		"title": title,
	    "btn_submit": btn_submit,
	    "form": form,
	    "confirm_message": confirm_message,
	    "lang_code": request.LANGUAGE_CODE
			}
	return render(request, "landings/landingpage_detail.html", context)



#function-based views
# def landing_list_view(request):
# 	queryset = LandingPage.objects.all()
# 	context = {
# 		"object_list": queryset,
# 	} 
# 	return render(request, "landings/landing_list.html", context)

# def landing_create_view(request):
# 	form = LandingPageForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()
# 		form = LandingPageForm()
# 	context = {
# 		'form': form,

# 	}
# 	return render(request, "landings/landing_create.html", context)

# def landing_detail_view(request,id):
# 	#obj = LandingPage.objects.get(id=1)
# 	obj = get_object_or_404(LandingPage, id=id)
# 	context = {
# 		'object': obj,

# 	}
# 	return render(request, "landings/landing_detail.html", context)
