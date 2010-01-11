from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import *

from django.core.urlresolvers import reverse

from django.views.generic.create_update import create_object, delete_object, update_object
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template

from ironticketc.models import Company, Ticket, CSProfile, Address
from irontickets.forms import *
from irontickets.views import *

urlpatterns = patterns('oi.views',
    url(r'^$', object_list, {
        'queryset': Address.objects.all(),
        'template_name': 'address/address_index.html',
        'template_object_name': 'address',
    }, name='address'),

    url(r'^(?P<object_id>\d+)$', object_detail, {
        'queryset': Address.objects.all(),
        'template_name': 'address/address_detail.html',
        'template_object_name': 'ticket',
    }, name='addressdetail'),

    url(r'^(?P<object_id>\d+)/edit$', update_object, {
        'form_class': AddressForm,
        'login_required': True,
        'template_name': 'address/address_form.html',
        'template_object_name': 'address',
    }, name='addressedit'),

    url(r'^(?P<object_id>\d+)/delete$', delete_object, {
        'model': Address,
        'login_required': True,
        'template_name': 'address/address_delete.html',
        'post_delete_redirect': '/oi/', #BUG: http://code.djangoproject.com/ticket/7571
        'template_object_name': 'address',
    }, name='addressdelete'),

    url(r'^processlist/$', address_list_action_process, name='processaddresslist'),

    url(r'^new/$', address_new, name='addressnew'),

    url(r'^new/(?P<cid>\d+)/$', company_address_new, name='companyaddressnew'),
)
