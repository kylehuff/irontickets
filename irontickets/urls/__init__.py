from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import *
from django.contrib import comments
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from django.views.generic.create_update import create_object, delete_object, update_object
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template
from irontickets.models import Ticket, Company, CompanyType

urlpatterns = patterns('irontickets.views',
    url(r'^$', direct_to_template, {
        'template': 'irontickets/base.html',
        'extra_context': {
            'title': 'Home',
            'tickets': Ticket.objects.all,
            'tickets_opened': Ticket.objects.open_tickets,
            'tickets_closed': Ticket.objects.closed_tickets,
            'companies': Company.objects.all,
            'companytypes': CompanyType.objects.all,
            'contacts': User.objects.all,
        },
    }, name='home'),

    url(r'^about/$', direct_to_template, {
        'template': 'irontickets/about.html',
        'extra_context': {
            'title': 'About OpenIron...',
        },
    }, name='about'),

    (r'^my/', include('irontickets.urls.my')),
    (r'^account/', include('irontickets.urls.account')),
    (r'^ticket/', include('irontickets.urls.ticket')),
    (r'^company/', include('irontickets.urls.company')),
    (r'^user/', include('irontickets.urls.user')),
    (r'^report/', include('irontickets.urls.report')),
    (r'^help/', include('irontickets.urls.help')),

    (r'^comment/', include('django.contrib.comments.urls')),
    (r'^attachments/', include('attachments.urls')),
    (r'^avatar/', include('avatar.urls')),
)
