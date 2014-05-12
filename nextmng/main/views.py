from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from forms  import TestSubjectForm
from models import TestSubject


def home(request, template_name='main/index.html'):
    
    
    _tosend = {}
    
    if request.POST:
        
        form = TestSubjectForm(request.POST)
        
        if form.is_valid():
            new_subject = form.save()
            _tosend['id_assigned'] = new_subject.code
        
        else:
            
            _tosend['form'] = form
        
    else:
        
        if "id_assigned" in request.GET:
            _tosend["id_assigned"] = request.GET["id_assigned"]
            
    return render(request, template_name, _tosend)