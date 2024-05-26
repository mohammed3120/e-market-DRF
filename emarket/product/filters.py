import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    minprice = django_filters.filters.NumberFilter(field_name='price' or 0, lookup_expr='gte')
    maxprice = django_filters.filters.NumberFilter(field_name='price' or 2000, lookup_expr='lte')


    class Meta:
        model = Product
        fields = ('name','category', 'brand', 'minprice', 'maxprice')