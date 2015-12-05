import sys
from datetime import datetime

from django.http import HttpResponse
from django.conf import settings

from url_magic import makeView
makeView.APP_NAME = 'url_magic_test_app'

# This will map to /hello-world
@makeView()
def helloWorld(request):
    return HttpResponse('Hello world')


# this maps to the home page
@makeView('$^')
def hellWorld(request):
    return HttpResponse('Hell!! World!!')


# use this for debugging the generated URL maps
import json
print >> sys.stderr, json.dumps(dict(makeView.dctUrls), indent=4)