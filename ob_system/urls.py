from django.urls import path, include
from registration.backends.hmac.views import RegistrationView
from .forms import PoliceUserForm

from . import views


urlpatterns = [
    path('accounts/register', RegistrationView.as_view(form_class=PoliceUserForm),
         name='registration'),
    path('accounts/', include('registration.backends.hmac.urls')),


]