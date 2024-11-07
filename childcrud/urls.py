from django.urls import re_path


from childcrud.views import ajax_create_update, ajax_list, fk_create_update

urlpatterns = [
    re_path(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/$', ajax_list, name='childcrud-list'),
    re_path(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/$', ajax_create_update, name='childcrud-update'),
    re_path(r'(?P<p_app_name>\w+)/(?P<p_model_name>\w+)/(?P<p_id>\d+)/(?P<app_name>\w+)/(?P<model_name>\w+)/new/$', ajax_create_update, name='childcrud-create'),
    re_path(r'(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<id>\d+)/$', fk_create_update, name='fk-update'),
    re_path(r'(?P<app_name>\w+)/(?P<model_name>\w+)/$', fk_create_update, name='fk-create'),
]
