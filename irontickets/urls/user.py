from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, delete_object, update_object
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import UserChangeForm

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.utils.functional import lazy
reverse_lazy = lazy(reverse, unicode)

from irontickets.views.user import user_new, user_detail

urlpatterns = patterns('irontickets.views',
    url(r'^$', login_required(object_list), {
        'queryset': User.objects.all(),
        'template_name': 'irontickets/user/user_list.html',
        'allow_empty': True,
        'template_object_name': 'user',
        'extra_context': {
            'title': 'User List',
        },
    }, name = 'users'),
    
    url(r'^new/$', user_new, name='usernew'),
    
    url(r'^(?P<object_id>\d+)/$', login_required(object_detail), {
        'queryset': User.objects.all(),
        'template_name': 'irontickets/user/user_detail.html',
        'template_object_name': 'usr',
        'extra_context': {
            'title': 'User'
        },
    }, name='userdetail'),
    
    url(r'^(?P<object_id>\d+)/edit/$', update_object, {
        'model': User,
        'login_required': True,
        'template_name': 'irontickets/user/user_form.html',
        'template_object_name': 'usr',
    }, name='useredit'),
    
    url(r'^(?P<object_id>\d+)/delete/$', delete_object, {
        'model': User,
        'post_delete_redirect': reverse_lazy('users'),
        'login_required': True,
        'template_name': 'irontickets/user/user_delete.html',
        'template_object_name': 'usr',
        'extra_context': {
            'title': 'User'
        },
    }, name='userdelete'),
)
