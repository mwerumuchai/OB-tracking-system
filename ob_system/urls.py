from django.conf.urls import url
from . import views

urlpatterns=[
    #the landing url
    url(r'^$',views.index,name='index'),

    # occurrence book url
    url(r'^occurrence_book/',views.occurrence_book,name='occurrence_book'),

    # archives url
    url(r'^archives/',views.archives,name='archives'),

    # Cash bail book url
    url(r'^cash_bail_book',views.cash_bail,name='cash_bail')
]
