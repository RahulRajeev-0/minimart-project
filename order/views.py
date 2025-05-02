from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .models import Order, OrderItem
from customer.models import Customer
from .serializers import OrderSerializer, OrderItemSerializer

# service/ helper or utility function 
from .services import place_order


class OrderView(APIView):
    
    # create order (place order)
    def post(self, request):
        customer_id = request.data.get('customer_id', 0)
        items_data = request.data.get('items', [])
        try:
            customer = Customer.objects.get(id=customer_id)
        except Exception as e:
            print(e)
            return Response({"error": "Provide a valid customer_id"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            order = place_order(customer, items_data)
        except ValidationError as e:
            print(str(e))
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            OrderSerializer(order).data, 
            status=status.HTTP_201_CREATED
            )
        

    def patch(self, request):
        order_id = request.data.get("order_id")
        new_status = request.data.get("status")

        if not order_id or not new_status:
            return Response(
                {"error": "order_id and status are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = order.status
        
        if new_status not in dict(Order.STATUS_CHOICES):
                return Response(
                    {"error": "Invalid status value."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        with transaction.atomic():
            # If cancelling and wasn't already cancelled
            if new_status == 'cancelled' and old_status != 'cancelled':
                for item in order.items.all():
                    product = item.product
                    product.in_stock += item.qty
                    product.save()

            # If un-cancelling is allowed (optional reverse logic)
            elif old_status == 'cancelled' and new_status != 'cancelled':
                for item in order.items.all():
                    product = item.product
                    if product.in_stock < item.qty:
                        return Response(
                            {"error": f"Insufficient stock for product '{product.name}'."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    product.in_stock -= item.qty
                    product.save()

            order.status = new_status
            order.save()

        return Response({"message": f"Order status updated to {new_status}."}, 
                        status=status.HTTP_200_OK)
    
    
    def get(self, request):
        pass
    # change order status

        
    
    # soft delete order
    def delete(self, request):
        pass

