from django_filters.rest_framework import FilterSet
from .models import Product


class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      'collection_id': ['exact'], # exact number no a float
      'unit_price': ['gt', 'lt'],  # For a range including float
    } 