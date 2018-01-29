"""occurrence_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ob_system import views as core_views
from occurrence_book.settings import GeneratePDF
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('ob_system.urls')),

    path('', include('pwa.urls')),

    path('signup/', core_views.signup, name='signup'),

    path('login/', core_views.officer_login, name='login'),

    # path('pdf', TemplateView.as_view.GeneratePDF(template_name='pdf/cashbail.html'), name='pdf')

]

