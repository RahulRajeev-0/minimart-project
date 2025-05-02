from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .models import Order, OrderItem
from customer.models import Customer
from .serializers import OrderSerializer, OrderItemSerializer

# service/ helper or utility function 
from .services import (place_order, 
                       update_order_status, 
                       get_all_orders, 
                       get_order_by_id,
                       get_orders_by_customer_id)

# views 

class PlaceOrderView(APIView):
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
            return Response({"error": e.detail}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            OrderSerializer(order).data, 
            status=status.HTTP_201_CREATED
            )
    
# update/edit the order (change the status)
class OrderStatusUpdateView(APIView):
    def patch(self, request):
        order_id = request.data.get("order_id")
        new_status = request.data.get("status")

        if not order_id or not new_status:
            return Response(
                {"error": "order_id and status are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = update_order_status(order_id, new_status)
        except ValidationError as e:
            return Response({"error": e.detail}, 
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": f"Order status updated to {order.status}."},
            status=status.HTTP_200_OK
        )

# get all the orders 
class GetAllOrderView(APIView):
    def get(self, request):
        orders = get_all_orders()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# get a particular order details 
class GetOrderDetailView(APIView):
    def get(self, request, id):
        try:
            order = get_order_by_id(id)
        except Exception as e:
            return Response({"error": e.detail}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

#  for soft delete of order
class SoftDeleteOrderView(APIView):
    def delete(self, request, id):
        try:
            order = get_order_by_id(id)
        except Exception as e:
            return Response({"error": e.detail}, status=status.HTTP_404_NOT_FOUND)
        order.is_active = False
        order.save()
        return Response({"detail": "Product soft-deleted"}, 
                        status=status.HTTP_204_NO_CONTENT)

# for getting the orders of specific customer 
class CustomerOrdersView(APIView):
    def get(self, request, id):
        
        try:
            orders = get_orders_by_customer_id(id)
        except Exception as e:
            return Response({"error": e.detail},
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


