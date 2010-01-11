from irontickets.models import TicketStatus, TicketPriority
from django.contrib.auth.models import User

def tickets(request):
    """
    Adds ticket related context variables
    """
    return {
        'TICKET_STATUSES': TicketStatus.objects.all(),
        'TICKET_PRIORITIES': TicketPriority.objects.all().order_by('-priority'),
    }


def useraccounts(request):
    """
    Adds a context variable containing user accounts.
    """
    return {'USER_ACCOUNTS': User.objects.all()}


def employees(request):
    """
    Returns employees as defined by django.contrib.admin.
    """
    return {'EMPLOYEES': User.objects.filter(is_staff=True)}
