from django.urls import path
from . import views


app_name = 'testapp'

urlpatterns = [
    path('testapp/', views.post_lists, name='post_lists'),
    path('testapp/ajax_post_add/', views.ajax_post_add, name='ajax_post_add'),
]