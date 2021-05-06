from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from mailer import send_mail, send_html_mail
from django import forms

from landinghub.utils import check_in_memory_mime

from django.views.generic import (
	CreateView,
	DetailView,
	ListView,
	UpdateView,
	DeleteView,
	FormView,
)
from django.views.generic.edit import FormMixin

from .models import VirtualRoomPage, SessionMaterial, AttendeeVroom
from .forms import VirtualRoomPageForm, VirtualRoomMaterialUploaForm, VirtualRoomAttendeeForm

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
class VirtualRoomPageCreateView(LoginRequiredMixin, CreateView):
	template_name = 'virtualrooms/virtualroompage_create.html'
	form_class = VirtualRoomPageForm

	def dispatch(self, request, *args, **kwargs):
		return super(VirtualRoomPageCreateView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(VirtualRoomPageCreateView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = _('Create Virtual Room')
		context['title_action'] = _('Create Virtual Room Access Page')
		return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		#print(check_in_memory_mime(self.request.FILES['file']))
		actual_user = User.objects.get(username=self.request.user)
		instance.owner = actual_user
		# try:
		# 	instance.file_type = str(check_in_memory_mime(self.request.FILES['file']))
		# 	if instance.file_type.find('word') != -1:
		# 		instance.file_type = 'doc'
		# 	elif instance.file_type.find('spreadsheet') != -1:
		# 		instance.file_type = 'xls'
		# 	elif instance.file_type.find('powerpoint') != -1:
		# 		instance.file_type = 'ppt'
		# 	else:
		# 		pass
		# except Exception as e:
		#     print(e)
		instance.save()
		return super(VirtualRoomPageCreateView, self).form_valid(form)

class VirtualRoomPageUpdateView(LoginRequiredMixin, UpdateView):
	model = VirtualRoomPage
	form_class = VirtualRoomPageForm
	template_name = 'virtualrooms/virtualroompage_create.html'
	queryset = VirtualRoomPage.objects.all()
	#success_url ="/"
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		page = get_object_or_404(VirtualRoomPage, id=self.kwargs['pk'])
		if self.request.user == page.owner:
			pass
		else:
			return reverse('virtualrooms:virtualroom-list')
		return super(VirtualRoomPageUpdateView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(VirtualRoomPageUpdateView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		page = get_object_or_404(VirtualRoomPage, id=self.kwargs['pk'])
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['landing'] = page
		context['title'] = _('Update Virtual Room Page')
		context['title_action'] = _('Update Virtual Room Page')
		return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		#print(check_in_memory_mime(self.request.FILES['file']))
		actual_user = User.objects.get(username=self.request.user)
		instance.owner = actual_user
		# try:
		# 	instance.file_type = str(check_in_memory_mime(self.request.FILES['file']))
		# 	if instance.file_type.find('word') != -1:
		# 		instance.file_type = 'doc'
		# 	elif instance.file_type.find('spreadsheet') != -1:
		# 		instance.file_type = 'xls'
		# 	elif instance.file_type.find('powerpoint') != -1:
		# 		instance.file_type = 'ppt'
		# 	else:
		# 		pass
		# except Exception as e:
		#     print(e)
		instance.save()
		return super(VirtualRoomPageUpdateView, self).form_valid(form)

class VirtualRoomPageDeleteView(LoginRequiredMixin, DeleteView,):
	queryset = VirtualRoomPage.objects.all()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(VirtualRoomPageDeleteView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = '%s %s' %(_('Delete'), _('Virtual Room'))
		return context

	def get_success_url(self):
		return reverse('virtualrooms:virtualroom-list')

class VirtualRoomPageListView(LoginRequiredMixin, ListView):
	#template_name = ''
	#queryset = ''

	def get_context_data(self, **kwargs):
		context = super(VirtualRoomPageListView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = _('My Virtual Rooms')
		return context

	def get_queryset(self):
		queryset = VirtualRoomPage.objects.filter(owner=self.request.user).order_by('name')
		return queryset

def virtualroom_page(request, slug):
	context = {}
	landing = get_object_or_404(VirtualRoomPage, slug=slug)
	title = _("%s") %(landing.name)
	files = SessionMaterial.objects.filter(session=landing, active=True).order_by('-updated')
	context = {
	    "object": landing,
	    "files_list": files,
		"title": title,
			}
	return render(request, "virtualrooms/virtualroompage_detail.html", context)

class VirtualRoomMaterialUploadView(FormView):
	template_name = 'virtualrooms/virtualroom_material_edit_form.html'
	form_class = VirtualRoomMaterialUploaForm

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		virtualroom = get_object_or_404(VirtualRoomPage, id=self.kwargs['pk'])
		if self.request.user == virtualroom.owner:
			pass
		else:
			return reverse('virtualrooms:virtualroom-list')
		return super(VirtualRoomMaterialUploadView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
	    return reverse('virtualrooms:virtualroom-materials', kwargs={'pk': self.kwargs['pk']})

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(VirtualRoomMaterialUploadView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['title'] = _('Supporting Material')
		virtualroom = VirtualRoomPage.objects.get(id=self.kwargs['pk'])
		files = SessionMaterial.objects.filter(session=virtualroom).order_by('-updated')
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['activity'] = virtualroom
		context['files_list'] = files
		return context

	def form_valid(self, form):
	    virtualroom = VirtualRoomPage.objects.get(id=self.kwargs['pk'])
	    instance = form.save(commit=False)
	    instance.session = virtualroom
	    instance.file_type = check_in_memory_mime(self.request.FILES['file'])
	    if not instance.file_type == 'application/pdf':
	        if instance.file_type.find('word') != -1:
	            instance.file_type = 'doc'
	        elif instance.file_type.find('spreadsheet') != -1:
	            instance.file_type = 'xls'
	        elif instance.file_type.find('powerpoint') != -1:
	            instance.file_type = 'ppt'
	        else:
	            pass
	    instance.save()
	    messages.add_message(self.request, messages.SUCCESS, _('File saved correctly.'))
	    return super(VirtualRoomMaterialUploadView, self).form_valid(form)


class VirtualRoomAttendeeSignupView(SuccessMessageMixin, AjaxTemplateMixin, CreateView):
	template_name = 'virtualrooms/virtualroom_signup_form.html'
	form_class = VirtualRoomAttendeeForm
	success_url = reverse_lazy('home')

	def dispatch(self, request, *args, **kwargs):
	    landing = get_object_or_404(VirtualRoomPage, id=self.kwargs['pk'])
	    return super(VirtualRoomAttendeeSignupView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    context = super(VirtualRoomAttendeeSignupView, self).get_context_data(**kwargs)
	    context['landing_id'] = self.kwargs['pk']
	    context['main_header'] = _('Please enter your name and e-mail address to identify yourself and give you access to the virtual room.')
	    #context['sub_header'] = _('By subscribing to the Newsletter we will notify you of special discounts and new product launches')
	    form_btn_text = _("Send")
	    context['btn_submit'] = form_btn_text
	    return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		email = form.cleaned_data.get("email")
		fname = form.cleaned_data['name']
		if not form.cleaned_data['name']:
			fname = '-'
		instance.session = VirtualRoomPage.objects.get(id=self.kwargs['pk'])
		#phone = instance.phone_number
		instance.save()
		return HttpResponseRedirect(self.success_url)

class VirtualRoomAttendeeListView(LoginRequiredMixin, ListView):
	
	def get_context_data(self, **kwargs):
		context = super(VirtualRoomAttendeeListView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = _('Attendees Resgistrations')
		landing = get_object_or_404(VirtualRoomPage, id=self.kwargs['pk'])
		context['landing'] = landing
		return context

	def get_queryset(self):
		landing = get_object_or_404(VirtualRoomPage, id=self.kwargs['pk'])
		queryset = AttendeeVroom.objects.filter(session=landing).order_by('-timestamp')
		return queryset
