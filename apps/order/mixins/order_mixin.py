from apps.base.mixins.exception import StockInsufficient
from apps.order.constant import SHIPPED, DELIVERED
from apps.order.serializers import OrderItemSerializer


class OrderManagerMixin(object):

    @staticmethod
    def restore_order_items(order):
        """
        Restore stock quantities for the products associated with the order items and delete the order items.

        Args:
            order (Order): The order instance for which to restore stock quantities.

        Returns:
            None
        """

        # Check if the order is in a modifiable status
        if order.order_status not in [SHIPPED, DELIVERED]:

            # Retrieve all order items associated with the order
            order_items = order.order_items.all().select_related("product")

            # Iterate through each order item to restore stock quantities
            for order_item in order_items:

                # Retrieve the product from the order item
                product = order_item.product

                # Increase the stock quantity by the ordered quantity
                product.stock_quantity += order_item.quantity
                product.save()

            # Delete all order items associated with the order
            order_items.delete()

    def _process_order(self, serializer):
        """
        Perform custom actions during the creation of a new order.

        Args:
            serializer (OrderSerializer): The serializer instance for the order being created.

        Returns:
            None
        """

        # Extract the 'order_items' data from the validated serializer data
        order_items = serializer.validated_data.pop("order_items", None)

        # Check order item
        if order_items is not None:

            # Calculate the total price based on the order items
            total_price = sum(item['product'].price * item['quantity'] for item in order_items)

            # Save the order with the user and total price
            order = serializer.save(user=self.request.user, total_price=total_price)

            # Update stock quantities and save each order item
            for item in order_items:
                # Retrieve the product from the order item
                product = item["product"]

                # Check if there is sufficient stock for the order item
                if product.stock_quantity >= item["quantity"]:
                    # Reduce the stock quantity by the ordered quantity
                    product.stock_quantity -= item["quantity"]
                    product.save()
                else:
                    # If stock quantity is insufficient, raise an exception
                    raise StockInsufficient(f"Insufficient stock for #{product.id}-{product.name}")

                # Update the order item with the product ID and save it
                item["product"] = product.id

            # Create a serializer for the order items and save them with the associated order
            item_serializer = OrderItemSerializer(data=order_items, many=True)
            item_serializer.is_valid(raise_exception=True)
            item_serializer.save(order=order)
        else:
            serializer.save(user=self.request.user, total_price=0.0)
