from django.conf.urls import url
from .views import ajax_create_update, ajax_list, fk_create_update

urlpatterns = (
    url(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/$', ajax_list, name='childcrud-list'),
    url(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/$', ajax_create_update, name='childcrud-update'),
    url(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/new/$', ajax_create_update, name='childcrud-create'),
    url(r'(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/$', fk_create_update, name='fk-update'),
    url(r'(?P<app_name>\w+)/(?P<model_name>\w+)/$', fk_create_update, name='fk-create'),
)
