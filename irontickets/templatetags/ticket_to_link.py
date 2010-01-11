import re

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from irontickets.models import Ticket

class ReverseProxy:
    def __init__(self, sequence):
        self.sequence = sequence

    def __iter__(self):
        length = len(self.sequence)
        i = length
        while i > 0:
            i = i - 1
            yield self.sequence[i]

def ticket_to_link(text):
    if text == '':
        return text

    matches = []
    for match in re.finditer("#(\d+)", text):
        matches.append(match)

    for match in ReverseProxy(matches):
        start = match.start()
        end = match.end()
        number = match.groups()[0]
        url = reverse('ticketdetail', args=[number])
        try:
            ticket = Ticket.objects.get(pk=number)
        except Ticket.DoesNotExist:
            ticket = None

        if ticket:
            text = "%s<a href='%s'>#%s</a>%s" % (text[:match.start()], url, match.groups()[0], text[match.end():])
    return mark_safe(text)

register = template.Library()
register.filter(ticket_to_link)
