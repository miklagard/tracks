from django.conf.urls import url
from api import views

urlpatterns = [
    url('respond', views.respond.as_view()),
]