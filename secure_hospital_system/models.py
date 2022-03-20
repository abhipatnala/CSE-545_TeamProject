from django.db import models

from django.contrib.auth.models import User

import django_tables2 as tables
import django_filters



class UserTable(tables.Table):
    class Meta:
        model = User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username']



