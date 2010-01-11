from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('irontickets.views',
    url(r'^$', direct_to_template, {
        'template': 'irontickets/base.html',
        'extra_context': {
            'title': 'Help',
        },
    }, name='help'),
)
