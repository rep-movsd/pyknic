from django.conf.urls import patterns, include, url

# Dont change the order of this
from url_magic import makeView
makeView.APP_NAME = 'url_magic_test_app'

import url_magic_test_app.views


# URLs from views.py that are registered via the makeView decorator
urlpatterns = patterns('', * makeView.dctUrls.items())
