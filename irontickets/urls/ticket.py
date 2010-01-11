from django.conf.urls.defaults import *

from django.views.generic.create_update import create_object, delete_object, update_object
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, unicode)

from irontickets.forms import TicketForm, TicketStatusForm, TicketEditForm
from irontickets.models import Ticket
from irontickets.views.ticket import ticket_delete

from ajax_validation.views import validate

urlpatterns = patterns('irontickets.views',
    url(r'^$', login_required(object_list), {
        'queryset': Ticket.objects.all(),
        'paginate_by': 100,
        'template_name': 'irontickets/tickets/ticket_list.html',
        'allow_empty': True,
        'template_object_name': 'ticket',
        'extra_context': {
            'title': 'Ticket List',
        },
    }, name = 'tickets'),

    url(r'^new/$', create_object, {
        'form_class': TicketForm,
        'login_required': True,
        'template_name': 'irontickets/tickets/ticket_new.html',
        'extra_context': {
            'title': 'New Ticket'
        },
    }, name='ticketnew'),

    url(r'^(?P<object_id>\d+)/$', login_required(object_detail), {
        'queryset': Ticket.objects.all(),
        'template_name': 'irontickets/tickets/ticket_detail.html',
        'template_object_name': 'ticket',
        'extra_context': {
            'title': 'Ticket'
        },
    }, name='ticketdetail'),

    url(r'^(?P<object_id>\d+)/edit/$', update_object, {
        'form_class': TicketEditForm,
        'login_required': True,
        'template_name': 'irontickets/tickets/ticket_form.html',
        'template_object_name': 'ticket',
        'extra_context': {
            'title': 'Ticket'
        },
    }, name='ticketedit'),

    url(r'^(?P<object_id>\d+)/delete/$', ticket_delete, name='ticketdelete'),
    #BUG: Unable to call reverse from within urls.py, moved ticket_delete to views.py.  See: http://code.djangoproject.com/ticket/5925

    url(r'^(?P<object_id>\d+)/editstatus/$', update_object, {
        'form_class': TicketStatusForm,
        'login_required': True,
        'template_name': 'irontickets/tickets/ticket_form.html',
        'template_object_name': 'ticket',
    }, name='ticketstatusedit'),

    (r'^newajax/$', validate, {'form_class': TicketForm}, 'ticket_form_validate')
)
