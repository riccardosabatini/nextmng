from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

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



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
class S3Uploader(APIView):
    
    
    def get(self, request):
        
        from django.core.files.storage import default_storage as storage
        import random
        import string
        
        if 'name' not in request.GET:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        _rndlen    = 6
        _name      = request.GET['name']
        
        while True:
            _rnd       = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(_rndlen))
            _new_name  = _name+"-"+_rnd
            if not storage.exists(_name):
                break
        
        _post_form = self.generate_post_form(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_SECRET_ACCESS_KEY, _new_name, 'text/plain')
        
        return JSONResponse(_post_form)
        
    def generate_post_form(self, bucket_name, access_key, object_key, content_type):
        
        import hmac
        from hashlib import sha1
        from django.conf import settings
        import datetime
        
        TIMEOUT              = datetime.timedelta(seconds=1000)
        HTTP_CONNECTION_TYPE = "http"
        
        _success_status = "201"
        _acl            = "public-read"
        
        policy = """{"expiration": "%(expires)s","conditions": [{"bucket":"%(bucket)s"},["eq","$key","%(key)s"],{"acl":"%(acl)s"},{"success_action_status":"%(success_status)s"}]}"""
        policy = policy%{
          "expires":(datetime.datetime.utcnow()+TIMEOUT).strftime("%Y-%m-%dT%H:%M:%SZ"), # This has to be formatted this way
          "bucket": bucket_name, # the name of your bucket
          "key": object_key, # this is the S3 key where the posted file will be stored
          "content_type": content_type,
          "acl":_acl,
          "success_status":_success_status
        }
        
        encoded = policy.encode('utf-8').encode('base64').replace("\n","") # Here we base64 encode a UTF-8 version of our policy.  Make sure there are no new lines, Amazon doesn't like them.
        return ("%s://%s.s3.amazonaws.com/"%(HTTP_CONNECTION_TYPE, bucket_name),
                {"policy":encoded,
                 "signature":hmac.new(access_key,encoded,sha1).digest().encode("base64").replace("\n",""), # Generate the policy signature using our Amazon Secret Key
                 "key": object_key,
                 "AWSAccessKeyId": access_key, # Obviously the Amazon Access Key
                 "acl":_acl,
                 "success_action_status":_success_status,
                })
        