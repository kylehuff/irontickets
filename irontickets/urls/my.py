from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import *

from django.core.urlresolvers import reverse

from django.views.generic.create_update import create_object, delete_object, update_object
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('oi.views',
    url(r'^$', direct_to_template, {
        'template': 'irontickets/my/index.html',
        'extra_context': {
            'title': 'My Home',
        },
    }, name='myhome'),
#    url(r'^tickets/$', my_tickets, name='mytickets'),
#    url(r'^report/$', my_reports, name='myreports'),
#    url(r'^timecard/$', gndn, name='mytimecard'),
)
