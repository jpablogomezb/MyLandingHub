from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
	ListView,
)
#from .utils import get_mailchimp_api
from .forms import MoreInfoForm
from .models import MoreInfo
from landings.models import LandingPage

#Project Vars
project_logo = settings.PROJECT_LOGO
project_name = settings.PROJECT_NAME
project_domain = settings.PROJECT_DOMAIN
project_product_desc = settings.PRODUCT_DESCRIPTION

# Create your views here.

class MoreInfoListView(LoginRequiredMixin, ListView):
	
	def get_context_data(self, **kwargs):
		context = super(MoreInfoListView, self).get_context_data(**kwargs)
		context['project_logo'] = project_logo
		context['project_name'] = project_name
		context['title'] = _('More Information')
		activity = get_object_or_404(LandingPage, id=self.kwargs['pk'])
		context['landing'] = activity
		return context

	def get_queryset(self):
		#activity_id = self.kwargs['pk']
		activity = get_object_or_404(LandingPage, id=self.kwargs['pk'])
		#activity = .objects.get(id=activity_id)
		queryset = MoreInfo.objects.filter(obj_interest_id=activity.id).order_by('timestamp')
		#queryset = BookingMessage.objects.filter(booking=activity).order_by('-created')
		return queryset
