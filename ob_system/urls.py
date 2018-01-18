from django.urls import path, re_path
from . import views
from ob_system import views as core_views


urlpatterns = [

    # the landing url
    path('', views.index,name='index'),

    # occurrence book url
    path('occurrence_book/', views.occurrence_book,name='occurrence_book'),

    # archives url
    path('archives/', views.archives, name='archives'),

    # Cash bail book url
    path('cash_bail_book', views.cash_bail, name='cash_bail'),

    re_path(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            core_views.activate, name='activate'),

    path('search/', views.search_results, name='search_results'),

    path('occurrence_book/book/', views.book, name='book'),

    path('occurrence_book/report/', views.report, name='report'),

    path('occurrence_book/create-criminal-profile/', views.create_criminal_profile,
         name='create-criminal-profile'),

    path('cash-bail-book/', views.cashbailform, name='bail'),

    path('criminal/profile/<int:id>/', views.criminal_profile, name='criminal-profile'),
]
