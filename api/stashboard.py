from stashboardmodels import Service, ServiceStatus
from stashboardutils import get_info, set_status, create_service
from nebrios_authentication import oauth_required
import json


@oauth_required(realm='stashboard')
def update_status(request):
    try:
        service = request.POST.service
        return set_status(request.POST)
    except:
        try:
            service = request.BODY['service']
            return set_status(request.BODY)
        except:
            try:
                service = json.loads(request.BODY)['service']
                return set_status(json.loads(request.BODY))
            except:
                return HttpResponseBadRequest


def form_update_status(request):
    try:
        if request.is_authenticated:
            return set_status(request.FORM)
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest


@oauth_required(realm='stashboard')
def get_services(request):
    return Service.filter()


def form_get_services(request):
    try:
        if request.is_authenticated:
            return Service.filter()
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest


def form_get_services_options(request):
    try:
        if request.is_authenticated:
            return [{'value': service.name, 'label': service.name} for service in Service.filter()]
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest


@oauth_required(realm='stashboard')
def get_service_status_history(request):
    try:
        service = request.POST.service
    except:
        try:
            service = json.loads(request.BODY)['service']
        except:
            try:
                service = request.BODY['service']
            except:
                return HttpResponseBadRequest
    return get_info(service=service)


def test(request):
    return {'lol': 'foo'}


def form_get_service_status_history(request):
    try:
        if request.is_authenticated:
            return get_info(service=request.FORM.service)
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest


@oauth_required(realm='stashboard')
def get_services_statuses(request):
    return get_info()


def form_get_services_statuses(request):
    try:
        if request.is_authenticated:
            return get_info()
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest


def form_get_last4_statuses(request):
    try:
        if request.is_authenticated:
            return get_info(service=None, display=True)
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest


@oauth_required(realm='stashboard')
def new_service(request):
    try:
        name = request.POST.name
        return create_service(request.POST)
    except:
        try:
            name = request.BODY['name']
            return create_service(request.BODY)
        except:
            try:
                name = json.loads(request.BODY)['name']
                return create_service(json.loads(request.BODY))
            except:
                return HttpResponseBadRequest


def form_new_service(request):
    try:
        if request.is_authenticated:
            return create_service(request.FORM)
        else:
            return HttpResponseForbidden
    except:
        return HttpResponseBadRequest
