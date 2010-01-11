from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('irontickets.views',
    url(r'^signin/$', login, {'template_name': 'irontickets/account/signin.html'}, name='signin'),
    url(r'^signout/$', logout, {'template_name': 'irontickets/account/signout.html'}, name='signout'),
    url(r'^password/$', password_change, {'template_name': 'irontickets/account/password.html'}, name='password'),
    url(r'^password/done/$', password_change_done, {'template_name': 'irontickets/account/password_done.html'}, name='passworddone'),
    url(r'^password/reset/$', password_reset, {'template_name': 'irontickets/account/password_reset.html', 'email_template_name': 'irontickets/account/password_reset_email.html'}, name='passwordreset'),
    url(r'^password/reset/done/$', password_reset_done, {'template_name': 'irontickets/account/password_reset_done.html'}, name='passwordresetdone'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'irontickets/account/password_reset_confirm.html'}, name='passwordresetconfirm'),
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'irontickets/account/password_reset_complete.html'}, name='passwordresetcomplete'),
)
