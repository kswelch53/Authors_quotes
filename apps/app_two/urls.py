
# This is APP 2

#app-level url code:
from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index, name="index"),
    url(r'^add_favquote/(?P<quote_id>\d+)$', views.add_favquote, name="add_favquote"),
    url(r'^remove_quote/(?P<favquote_id>\d+)$', views.remove_quote, name="remove_quote"),
    url(r'^contribute_quote$', views.contribute_quote, name="contribute_quote"),
    url(r'^users/(?P<user_id>\d+)$', views.users, name="users"),
#    url(r'^admin/', admin.site.urls),
]
