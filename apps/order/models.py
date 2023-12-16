from apps.order.constant import PENDING, SHIPPED, CANCELED, DELIVERED
from apps.product.models import Product
from apps.base.models import BaseModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


ORDER_STATUS_CHOICES = [
    ('pending', _(PENDING)),
    ('shipped', _(SHIPPED)),
    ('delivered', _(DELIVERED)),
    ('canceled', _(CANCELED)),
]


class Order(BaseModel):
    """
    A model representing an order placed by a user.

    Attributes:
        user (User): The user who placed the order.
        products (Product, many-to-many through OrderItem): The products included in the order.
        total_price (Decimal): The total price of the order.
        order_status (str, choices): The status of the order, chosen from predefined status options.

    Methods:
        __str__(): Returns a string representation of the order, including its ID and the username of the user.

    Example:
        # Creating an order
        order = Order.objects.create(user=my_user, total_price=100.00, order_status='pending')

        # Adding products to the order using the 'products' field
        product1 = Product.objects.create(name='Product 1', description='...', price=50.00, stock_quantity=10)
        product2 = Product.objects.create(name='Product 2', description='...', price=30.00, stock_quantity=20)
        product3 = Product.objects.create(name='Product 3', description='...', price=20.00, stock_quantity=30)

        # Adding products to the order through the many-to-many relationship
        order.items.add(product1, through_defaults={'quantity': 2})  # Adding 2 units of Product 1
        order.items.add(product2, through_defaults={'quantity': 1})  # Adding 1 unit of Product 2
        order.items.add(product3.id, through_defaults={'quantity': 4})  # Adding 4 units of Product 3 (using id)

        # Adding products to the order through the many-to-many relationship (in different way)
        # It would be better to add products to the order through the many-to-many relationship (for both add or update)
        order.items.set([product1.id, product2.id, product3.id], through_defaults=[{'quantity': 2}, {'quantity': 3}, {'quantity': 4}])

        # Accessing OrderItem instances for a particular order
        order_items = order.order_items.all()
        for order_item in order_items:
            print(order_item.product.name, order_item.quantity)

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # items = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(BaseModel):
    """
    A model representing an item within an order.

    Attributes:
        order (Order): The order to which the item belongs.
        product (Product): The product included in the item.
        quantity (int): The quantity of the product in the order item.

    Methods:
        __str__(): Returns a string representation of the order item, including the quantity, product name, and order ID.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
