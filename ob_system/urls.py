from django.urls import path
from . import views


urlpatterns = [

    # the landing url
    path('',views.index,name='index'),

    # occurrence book url
    path('occurrence_book/',views.occurrence_book,name='occurrence_book'),

    # archives url
    path('archives/',views.archives,name='archives'),

    # Cash bail book url
    path('cash_bail_book',views.cash_bail,name='cash_bail')
]
