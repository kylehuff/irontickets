from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.context import RequestContext
from django.views.generic.list_detail import object_list

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from irontickets.models import Ticket, ITProfile, Company
from irontickets.forms import TicketForm, NewUserForm


@login_required
def user_list(request):
    return object_list(
        request,
        queryset = userlist,
        template_name = 'irontickets/user/user_list.html',
        allow_empty = True,
        template_object_name = 'user',
        extra_context = {'title': 'User List'},
    )


@login_required
def user_new(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        if user_form.is_valid():
            user = User(
                username = user_form.cleaned_data['Email'].split('@')[0],
                first_name = user_form.cleaned_data['FirstName'],
                last_name = user_form.cleaned_data['LastName'],
                email = user_form.cleaned_data['Email'],
            )
            user.set_password(user_form.cleaned_data['Password'])
            #BUG: Deal with two users with the same user part but different domain parts.
            # I.E. ann@example.tld and ann@company.tld will break this.
            user.save()
            prof = ITProfile(
                user = user,
                Title = user_form.cleaned_data['Title'],
                JobTitle = user_form.cleaned_data['JobTitle'],
                Company = user_form.cleaned_data['Company'],
            )
            prof.save()
            return HttpResponseRedirect(reverse('users'))
        else:
            print 'Failed validation'
    else:
        user_form = NewUserForm()
        
    return render_to_response('irontickets/user/user_form.html', {
        'form': user_form,
    }, context_instance=RequestContext(request))


def user_detail(request, object_id):
    #STUB: Redirects to django-admin user editor
    return HttpResponseRedirect(reverse('admin:auth_user_change', args=[object_id]))


@login_required
def user_new_ticket(request, object_id):
    contact_id = object_id
    contact = get_object_or_404(Contact, pk=contact_id)
    
    t = Ticket(contact=contact, company=contact.Company)
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



