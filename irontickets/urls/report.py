from django.contrib.auth.views import *
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('irontickets.views',
    #Basic Pages
    url(r'^$', direct_to_template, {
        'template': 'irontickets/reports/main.html',
        'extra_context': {
            'title': 'Reports',
        },
    }, name='reports'),
)

