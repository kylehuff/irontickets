from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.context import RequestContext
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import create_object, delete_object, update_object

from django.contrib.auth.decorators import login_required

from irontickets.models import Ticket, Company
from irontickets.forms import TicketForm


@login_required
def company_ticket_new(request, object_id):
    company_id = object_id
    company = get_object_or_404(Company, pk=company_id)
    
    t = Ticket(company=company)
    if request.method == 'POST':
        ticketform = TicketForm(request.POST, instance=t)
        if ticketform.is_valid():
            ticket = ticketform.save()
            return HttpResponseRedirect(reverse('ticketdetail', args=[ticket.pk]))
    else:
        ticketform = TicketForm(instance=t)

    return render_to_response(
        'irontickets/tickets/ticket_new.html',
        {'form': ticketform},
        context_instance=RequestContext(request)
    )


@login_required
def company_ticket_list(request, object_id):
    company = get_object_or_404(Company, pk=object_id)
    tickets = company.ticket_set.all()
    return object_list(
        request,
        queryset = tickets,
        template_name = 'irontickets/tickets/ticket_list.html',
        allow_empty = True,
        template_object_name = 'user',
        extra_context = {
            'title': '%s Ticket List' %(company.name)
        },
    )

