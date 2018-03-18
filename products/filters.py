from django.contrib.auth.models import User
import django_filters
from .models import Item


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ['ItemCategory']