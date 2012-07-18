from django.conf.urls.defaults import *

from views import ajax_create_update, ajax_list

urlpatterns = patterns('',
    url(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/$', ajax_list, name='childcrud-list'),
    url(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/$', ajax_create_update, name='childcrud-update'),
    url(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/new/$', ajax_create_update, name='childcrud-create'),
)