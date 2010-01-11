from django.core.urlresolvers import reverse
from django.views.generic.create_update import delete_object

from django.contrib.auth.decorators import login_required

from irontickets.models import Ticket

@login_required
def ticket_delete(request, object_id):
    # This is here because we can't call reverse in views.py before reverse knows about views.py
    return delete_object(
        request,
        object_id = object_id,
        model = Ticket,
        post_delete_redirect = reverse('tickets'),
        login_required = True,
        template_name = 'irontickets/tickets/ticket_delete.html',
        template_object_name = 'ticket',
        extra_context = {
            'title': 'Ticket'
        })

