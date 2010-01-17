from django.conf import settings
from django import template
from django.template.defaulttags import IfNode, TemplateIfParser

register = template.Library()

def do_ifloaded(parser, token):
    bits = token.split_contents()[1:]
    print parser
    print bits

    for app in settings.INSTALLED_APPS:
        if bits == app:

    var = TemplateIfParser(parser, bits).parse()
    nodelist_true = parser.parse(('else', 'endif'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfNode('', nodelist_true, nodelist_false)
do_if = register.tag("ifloaded", do_ifloaded)

