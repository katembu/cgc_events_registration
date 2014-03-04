from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from events import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myevent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^incomingsms/?$', views.incomingsms),
)
