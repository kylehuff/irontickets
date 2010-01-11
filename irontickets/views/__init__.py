from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

def show404(request):
        return render_to_response(
            'irontickets/404.html',
            context_instance=RequestContext(request)
        )

def show500(request):
        return render_to_response(
            'irontickets/500.html',
            context_instance=RequestContext(request)
        )
