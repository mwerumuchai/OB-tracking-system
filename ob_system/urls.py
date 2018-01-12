from django.conf.urls import url
from . import views

urlpatterns=[
    #the landing page
    url(r'^$',views.index,name='index'),

    # occurrence book page
    url(r'^ob/',views.occurrence_book,name='occurrence_book')
]
