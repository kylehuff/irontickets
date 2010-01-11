import re
from django import template
from django.core.urlresolvers import reverse

#BUG: Needs to be rewritten as a full template tag so we don't have to pass 'request' in each page

register = template.Library()
@register.simple_tag
def active(request, name, returnstring='active', descendents=True):
    '''
    *request* (required): the HTTP Request Object
    *name* (optional): Name of a view from urlconf.
    *returnstring* (optional): string to return on a match.  Defaults to 'active'
    *descendents* (optional): True causes 
    '''
    if descendents:
        if reverse(name) in request.path[0:]:
            return returnstring
    else:
        if reverse(name) == request.path[0:]:
            return returnstring

    return ''
    
