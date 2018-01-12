from django.conf.urls import url
from . import views

urlpatterns=[
    #the landing page
    url(r'^$',views.index,name='index')
]
