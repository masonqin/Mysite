from django.conf.urls import patterns, include, url
from django.contrib import admin



urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('mysite.views',

  ('^hello/$', 'hello'),
  ('^time/$', 'current_datetime'),
  (r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
  ('bootstrap','bootstrap_index'),

)

urlpatterns += patterns('books.views',

    ('^echo/$','display_meta'),
    ('^search-form','search'),
    ('ajaxTest','ajax'),
    url(r'^add/$', 'add', name='add'),
    url(r'^ajax_list/$', 'ajax_list', name='ajax-list'),
    url(r'^ajax_dict/$', 'ajax_dict', name='ajax-dict'),
    url(r'^get_pic/$', 'get_pic', name='get_pic'),
)
