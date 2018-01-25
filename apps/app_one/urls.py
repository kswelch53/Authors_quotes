
# This is APP1

#app-level url code:
from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
#    url(r'^admin/', admin.site.urls),
]
