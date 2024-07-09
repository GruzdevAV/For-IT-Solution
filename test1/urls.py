from django.urls import include, re_path

from . import views

app_name = 'test1'

urlpatterns = [
    re_path(r'^(video_maker)?$', views.video_maker, name='video_maker'),
]