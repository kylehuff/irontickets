from django.conf import settings
from django import template
from django.template import NodeList

register = template.Library()

def do_ifloaded(parser, token):
    bits = token.split_contents()[1:]
    print 'bits'
    print bits[0]
    var = bits[0]
    nodelist_true = parser.parse(('else', 'endifloaded'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifloaded',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfLoadedNode(var, nodelist_true, nodelist_false)
register.tag('ifloaded', do_ifloaded)


class IfLoadedNode(template.Node):
    def __init__(self, var, nodelist_true, nodelist_false=None):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.var = var
    
    def __repr__(self):
        return '<IfLoaded node>'
    
    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node
    
    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        nodes.extend(self.nodelist_true.get_nodes_by_type(nodetype))
        nodes.extend(self.nodelist_false.get_nodes_by_type(nodetype))
        return nodes
    
    def render(self, context):
        for app in settings.INSTALLED_APPS:
            print 'comparing [%s] and [%s]' %(str(app), str(self.var))
            if str(app) == str(self.var):
                return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

