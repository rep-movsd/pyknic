'''
Django URL automagic mapper
===========================

What is it?
-----------
A trivial decorator that when applied to a view function, automatically makes
that view available as a URL without having to edit urls.py

How does it work?
-----------------
We have a simple dictionary to which we add a URL to function mapping when the
decorator is encountered. camelCase view functions are converted to dashed-urls


How to use?
-----------
Import this module and the views module in your models file
Set the makeView.APP_NAME to the application name
Add @makeView before each view function. The URL is generated from the 
view function name : For example - someGreatViewFunction becomes a URL of the 
form - /some-great-view-function
If you want to manually specify the URL, just specify it as a parameter to the
decorator

Modify your urls.py similar to below, changing as necessary to suit your app
...............................................................................
from url_magic import makeView
import url_magic_test_app.views
urlpatterns = patterns('', * makeView.dctUrls.items())
...............................................................................

Add (changing the name of your app)
...............................................................................
import url_magic
url_magic.makeView.APP_NAME = 'url_magic_test_app'
...............................................................................
At the top of your views.py

Note that url_magic needs to be in your path for both the main django folder 
and the app folder.
You can add 
...............................................................................
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
...............................................................................
to your settings.py as I've done here


Why is this useful?
-------------------
You can add a view to a django website just by writing the view function, and 
your urls.py becomes really simple


How to handle multiple django apps in a project?
------------------------------------------------
Not supported yet.


'''

import sys
import re

from functools import wraps
from collections import OrderedDict

# Thanks to stackoverflow for the camelcase to dashed-format-url conversion
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camelToURL(name):
    '''
    Convert camelCase to dashed-format-url-thing
    '''
    s1 = first_cap_re.sub(r'\1-\2', name)
    return all_cap_re.sub(r'\1-\2', s1).lower()


class makeView(object):
    '''
    Decorator that adds a view function to the django URL map
    '''
    dctUrls = OrderedDict()
    APP_NAME = '';

    def __init__(self, url=None):
        self.url = url

    def __call__(self, func):
        @wraps(func)
        def wrappee(*args, **kwargs):
            return func(*args, **kwargs)

        # If URL was unspecified, create it from the camelCase name of the view
        if not self.url:
            url = '^' + camelToURL(func.__name__)
        else:
            url = self.url

        # add the mapping to our dict
        makeView.dctUrls[url] = self.APP_NAME + '.views.' + func.__name__

        return wrappee
