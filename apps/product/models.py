from django.db import models
from apps.base.models import BaseModel
from django.conf import settings


class ProductCategory(BaseModel):
    """
    A model representing product categories.

    Attributes:
        parent (Category, optional): The parent category to which this category belongs (can be blank or null).
        name (str): The name of the category.
        description (str, optional): A textual description of the category (can be blank).

    Methods:
        __str__(): Returns a string representation of the category, which is its name.
    """

    parent = models.ForeignKey("self", related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """
    A model representing products available in the inventory.

    Attributes:
        name (str): The name of the product.
        description (str): A detailed description of the product.
        price (Decimal): The price of the product.
        stock_quantity (int): The available quantity of the product in the inventory.
        categories (Category, many-to-many): The categories to which the product belongs.
        images (ImageField, optional): An image representing the product (can be blank or null).

    Methods:
        __str__(): Returns a string representation of the product, which is its name.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(ProductCategory, related_name='products', blank=True)
    images = models.ImageField(upload_to='product/images/', blank=True, null=True)

    def __str__(self):
        return self.name


RATING_CHOICES = [
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
]


class ProductReview(BaseModel):
    """
    Represents a review for a product written by a user.

    Attributes:
        user (User): The user who wrote the review (foreign key relationship with the User model).
        product (Product): The product being reviewed (foreign key relationship with the Product model).
        text (str): The text content of the review.
        rating (int): The rating given by the user, representing the review's overall satisfaction level.
            Choices: 1 - '1 Star', 2 - '2 Stars', 3 - '3 Stars', 4 - '4 Stars', 5 - '5 Stars'.

    Methods:
        __str__(): Returns a string representation of the review, including the username and product name.

    Example:
        >>> review = ProductReview(user=my_user, product=my_product, text="Excellent product!", rating=5)
        >>> print(review)
        Review by username for Product Name
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Product")
    text = models.TextField(verbose_name="Review Text")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, verbose_name="Rating")

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
