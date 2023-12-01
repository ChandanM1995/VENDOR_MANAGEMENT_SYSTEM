from datetime import timezone
from . models import Vendor, PurchaseOrder, HistoricalPerformance
from . serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, SimpleVendorSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.db.models.aggregates import Avg


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer



class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vendor']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({'acknowledged': True})
    
    def recalculate_vendor_performance(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivery_count = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()
        vendor.on_time_delivery_rate = (on_time_delivery_count / total_completed_pos) * 100 if total_completed_pos > 0 else 0


        avg_quality_rating = completed_pos.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg']
        vendor.quality_rating_avg = avg_quality_rating if avg_quality_rating is not None else 0


        acknowledged_pos = completed_pos.filter(acknowledgment_date__isnull=False)
        avg_response_time = acknowledged_pos.aggregate(Avg('acknowledgment_date' - 'issue_date'))['acknowledgment_date__avg']
        vendor.average_response_time = avg_response_time.total_seconds() if avg_response_time is not None else 0


        successful_fulfillment_count = completed_pos.filter(status='completed', issues__isnull=True).count()
        vendor.fulfillment_rate = (successful_fulfillment_count / total_completed_pos) * 100 if total_completed_pos > 0 else 0

        vendor.save()
    


class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            performance_data = HistoricalPerformance.objects.filter(vendor=vendor)
            
            vendor_serializer = SimpleVendorSerializer(vendor)
            performance_serializer = HistoricalPerformanceSerializer(performance_data, many=True)

            return Response({
                'vendor_info': vendor_serializer.data,
                'performance_history': performance_serializer.data
            }, status=status.HTTP_200_OK)

        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)


