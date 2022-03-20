from django.views.generic import ListView
from .models import UserTable, User, UserFilter
import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class UserTableView(tables.SingleTableView):
    table_class = UserTable
    queryset = User.objects.all()
    template_name = "user_table.html"


class FilteredUserTableView(SingleTableMixin, FilterView):
    table_class = UserTable
    model = User
    template_name = "user_filter_table.html"

    filterset_class = UserFilter

