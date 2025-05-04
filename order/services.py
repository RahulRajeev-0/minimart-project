'''
includes helper for order module 
'''
from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound
from product.models import Product
from order.models import Order, OrderItem 
from customer.models import Customer
#  helper functions 

@transaction.atomic
def place_order(customer, items_data):
    """
    helper for creating a order, and updating its stock value based on qty

    items_data = [
        {"product_id": 1, "qty": 2},
        {"product_id": 3, "qty": 1}
    ]
    """

    if not items_data:
        raise ValidationError("No items provided.")
    

    if not customer:
        raise ValidationError("No customer found")
    

    order = Order.objects.create(customer=customer)

    # creating order items data based on qty and product
    for item in items_data:
        try:
            product = Product.objects.select_for_update().get(id=item["product_id"], is_active=True)
        except Product.DoesNotExist:
            raise ValidationError(f"Product with ID {item['product_id']} not found.")
        
        qty = int(item.get("qty", 0))
        if qty <= 0:
            raise ValidationError(f"Invalid quantity for product {product.name}.")
        
        if product.in_stock < qty:
            raise ValidationError(f"Not enough stock for product: {product.name}")
        
        product.in_stock -= qty
        product.save()

        OrderItem.objects.create(
            order=order,
            product=product,
            qty=qty,
            unit_price=product.discounted_price  # or `product.cost` as per business
        )

    return order


# change order status helper
def update_order_status(order_id, new_status):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise ValidationError("Order not found.")

    old_status = order.status

    if new_status not in dict(Order.STATUS_CHOICES):
        raise ValidationError("Invalid status value.")

    with transaction.atomic():
        if new_status == 'cancelled' and old_status != 'cancelled':
            for item in order.items.all():
                product = item.product
                product.in_stock += item.qty
                product.save()

        elif old_status == 'cancelled' and new_status != 'cancelled':
            for item in order.items.all():
                product = item.product
                if product.in_stock < item.qty:
                    raise ValidationError(f"Insufficient stock for '{product.name}'.")
                product.in_stock -= item.qty
                product.save()

        order.status = new_status
        order.save()

    return order


def get_all_orders():
    return Order.objects.prefetch_related('items', 'items__product').filter(is_active=True)


def get_order_by_id(order_id):
    try:
        return Order.objects.prefetch_related('items', 'items__product').get(id=order_id, is_active=True)
    except Order.DoesNotExist:
        raise NotFound("Order not found.")
    

def get_orders_by_customer_id(customer_id):
    return Order.objects.prefetch_related('items', 'items__product')\
        .filter(customer_id=customer_id, is_active=True)
