from django_filters.rest_framework import FilterSet
from . models import PurchaseOrder

class PurchageOrderFilter(FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = {
            'vendor__name' : ['exact'],
            # "delivery_date": ['gt', 'lt']
        }
