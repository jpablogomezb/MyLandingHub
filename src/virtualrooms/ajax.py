import json
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _


from .models import VirtualRoomPage, SessionMaterial


def delete_session_material_post(request):
    if request.method == 'POST' and request.is_ajax():
        material_id = request.POST.get('id')
        try:
            session_material = SessionMaterial.objects.get(id=int(material_id))
            session_material.delete()
            data = {}
            msg = _("Material deleted correctly.")
            data['status'] = 1
            data['result'] = msg

            return HttpResponse(
                json.dumps(data),
                content_type="application/json")

        except Exception as e:
            print(e)
            error = _('Oops! It seems that it is not possible to perform this action now, please try again later.')
            data = {'status': 0, 'error': error }
            return HttpResponse(json.dumps(data), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"Bad request": "service not available"}),
            content_type="application/json"
        )

def active_session_material_post(request):
    if request.method == 'POST' and request.is_ajax():
        material_id = request.POST.get('id')
        try:
            session_material = SessionMaterial.objects.get(id=int(material_id))
            session_material.active = True
            session_material.save()
            data = {}
            msg = _("Active Material.")
            data['status'] = 1
            data['result'] = msg

            return HttpResponse(
                json.dumps(data),
                content_type="application/json")

        except Exception as e:
            print(e)
            error = _('Oops! It seems that it is not possible to perform this action now, please try again later.')
            data = {'status': 0, 'error': error }
            return HttpResponse(json.dumps(data), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"Bad request": "service not available"}),
            content_type="application/json"
        )

def inactive_session_material_post(request):
    if request.method == 'POST' and request.is_ajax():
        material_id = request.POST.get('id')
        try:
            session_material = SessionMaterial.objects.get(id=int(material_id))
            session_material.active = False
            session_material.save()
            data = {}
            msg = _("Inactive Material.")
            data['status'] = 1
            data['result'] = msg

            return HttpResponse(
                json.dumps(data),
                content_type="application/json")

        except Exception as e:
            print(e)
            error = _('Oops! It seems that it is not possible to perform this action now, please try again later.')
            data = {'status': 0, 'error': error }
            return HttpResponse(json.dumps(data), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"Bad request": "service not available"}),
            content_type="application/json"
        )