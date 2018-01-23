from django.contrib.auth.models import User
from .models import CriminalProfile
import django_filters


class SearchFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    pub_date = django_filters.NumberFilter(name='pub_date', lookup_expr='year')

    class Meta:

        model = CriminalProfile

        fields = ('name', 'id_no')


