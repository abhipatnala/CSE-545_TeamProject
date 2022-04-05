from functools import wraps
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from secure_hospital_system.helpers import twofaEnabled
# from core.helpers.flash import send_flash_error
from .models import SHSUser

def is_patient(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and role_name=='patient':
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render


def is_admin(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and role_name=='':
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render

def is_doctor(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and role_name=='doctor':
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render


def is_hospital_staff(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and role_name=='hospitalstaff':
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render


def is_lab_staff(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and role_name=='labstaff':
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render

def is_insurance_staff(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and role_name=='insurancestaff':
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render

def is_doc_or_labstaff(redirect_to='home', error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            shs_user =  SHSUser.objects.select_related().filter(user = request.user.id)
            role_name = ''
            if len(shs_user) > 0:
                role = shs_user[0].role_id
                role_name = role.role_name
            if request.user.is_authenticated and (role_name=='doctor' or role_name=='labstaff'):
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Unauthorized')
                    # send_flash_error(request, error_flash_message) # Replace by your own implementation

            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render

def twoFARequired(redirect_to='home',error_flash_message=None):
    def inner_render(fn):
        @wraps(fn)  # Ensure the wrapped function keeps the same name as the view
        def wrapped(request, *args, **kwargs):
            if twofaEnabled(request.user):
                return fn(request, *args, **kwargs)
            else:
                if error_flash_message:
                    messages.error(request, error_flash_message)
                else:
                    messages.error(request, 'Please setup 2 Factor Authentication to proceed.')
            return HttpResponseRedirect(reverse(redirect_to))
        return wrapped
    return inner_render

