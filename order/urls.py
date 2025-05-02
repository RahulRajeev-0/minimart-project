from django.urls import path
from . import views


urlpatterns = [
    path('place-order/', views.PlaceOrderView.as_view(), name='place-order'),
    path('order-status/', views.OrderStatusUpdateView.as_view(), name='change-order-status' ),
    path('orders/', views.GetAllOrderView.as_view(), name='order-list'),
    path('order-detail/<int:id>/', views.GetOrderDetailView.as_view(), name='order-details'),
    path('order-delete/<int:id>/', views.SoftDeleteOrderView.as_view(), name='delete-order'),
]


