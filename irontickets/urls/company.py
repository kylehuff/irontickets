from django.contrib.auth.views import *
from django.conf.urls.defaults import *

from django.views.generic.create_update import create_object, delete_object, update_object
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template

from irontickets.forms import CompanyForm
from irontickets.models import Company
from irontickets.views.company import company_ticket_list, company_ticket_new

urlpatterns = patterns('irontickets.views',
    url(r'^$', object_list, {
        'queryset': Company.objects.active(),
        'paginate_by': 100,
        'template_name': 'irontickets/companies/company_list.html',
        'allow_empty': True,
        'template_object_name': 'company',
        'extra_context': {
            'title': 'Company List',
        },
    }, name = 'companies'),

    url(r'^new/$', create_object, {
        'form_class': CompanyForm,
        'login_required': True,
        'template_name': 'irontickets/companies/company_new.html',
        'extra_context': {
            'title': 'New Company'
        },
    }, name='companynew'),

    url(r'^(?P<object_id>\d+)/$', login_required(object_detail), {
        'queryset': Company.objects.all(),
        'template_name': 'irontickets/companies/company_detail.html',
        'template_object_name': 'company',
    }, name='companydetail'),

    url(r'^(?P<object_id>\d+)/edit/$', update_object, {
        'form_class': CompanyForm,
        'login_required': True,
        'template_name': 'irontickets/companies/company_form.html',
        'template_object_name': 'company',
    }, name='companyedit'),

    url(r'^(?P<object_id>\d+)/ticket/$', login_required(company_ticket_list), name = 'companyticketlist'),
    url(r'^(?P<object_id>\d+)/ticket/new/$', login_required(company_ticket_new), name = 'companyticketnew'),

)
