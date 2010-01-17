import datetime
from haystack import indexes
from haystack import site
from irontickets.models import Ticket

class TicketIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

site.register(Ticket, TicketIndex)

