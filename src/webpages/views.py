from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

#Project Vars
project_logo = settings.PROJECT_LOGO
project_name = settings.PROJECT_NAME
project_domain = settings.PROJECT_DOMAIN
project_product_desc = settings.PRODUCT_DESCRIPTION

# Create your views here.
def home_view(request, *args, **kwargs):
	context = {
		"project_name": project_name,
		"project_logo": project_logo,
	}
	return render(request, "home.html", context)


def landinghub_view(request, *args, **kwargs):
	context = {
		"project_name": project_name,
		"project_logo": project_logo,
	}
	return render(request, "landinghub.html", context)