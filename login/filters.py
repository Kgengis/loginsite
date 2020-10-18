from django_filters import FilterSet
from .models import Order
from django.forms import ModelForm
from django_filters import DateFilter, CharFilter


class OrderFilter(FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='gte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
