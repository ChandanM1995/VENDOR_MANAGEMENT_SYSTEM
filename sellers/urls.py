from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import VendorPerformanceAPIView, PurchaseOrderViewSet

# Create a router and register the viewsets

router = routers.DefaultRouter()
router.register('vendors', views.VendorViewSet)
router.register('purchase_orders', views.PurchaseOrderViewSet)


urlpatterns = [
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance-api'),
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderViewSet.as_view({'post': 'acknowledge'}), name='acknowledge-purchase-order'),
]

urlpatterns += router.urls







