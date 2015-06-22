from django.conf.urls import patterns, include, url
from django.contrib import admin

from mysite.views import hello,current_datetime,hours_ahead,bootstrap_index
from books.views import display_meta,search

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
   	('^hello/$', hello),
   	('^time/$', current_datetime),
   	(r'^time/plus/(\d{1,2})/$', hours_ahead),
   	('^echo/$',display_meta),
   	('^search-form',search),
   	('bootstrap',bootstrap_index),

    url(r'^admin/', include(admin.site.urls)),
)
