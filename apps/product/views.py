from rest_framework import viewsets
from .models import Product, ProductReview
from .serializers import ProductSerializer, ProductReviewSerializer


class ProductAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.

    This endpoint allows users to perform CRUD operations on products.

    - List all products created by the authenticated user.
    - Create a new product.
    - Retrieve, update, and delete a specific product.

    Responses:

    - GET request:
        - 200 OK: Returns a list of products created by the user.

    - POST request:
        - 201 Created: Returns the created product.
        - 400 Bad Request: If the request data is invalid.

    - GET, PUT, PATCH, DELETE requests:
        - 404 Not Found: If the product does not exist.
        - 403 Forbidden: If the user is not the creator of the product.


    Examples:
    - To list all products:
        ```http
        GET /products/
        ```

    - To create a new product:
        ```http
        POST /products/
        ```
        Payload:
        ```json
        {
            "name": "New Product",
            "description": "Product description",
            "price": 29.99,
            "stock_quantity": 100
        }
        ```

    - To retrieve a specific product:
        ```http
        GET /products/{id}/
        ```

    - To update a specific product:
        ```http
        PUT /products/{id}/
        ```
        Payload:
        ```json
        {
            "name": "Updated Product",
            "price": 39.99
        }
        ```

    - To delete a specific product:
        ```http
        DELETE /products/{id}/
        ```
    Note:

    * To create a new product (return status):
      - 201 Created: If the product is successfully created.
      - 400 Bad Request: If the request data is invalid.

    * To update a specific product (return status).
      - 200 OK: If the product is successfully updated.
      - 404 Not Found: If the product does not exist.
      - 403 Forbidden: If the user is not the creator of the product.
      - 400 Bad Request: If the request data is invalid.

    * To retrieve a specific product (return status).
      - 200 OK: If the product is successfully retrieved.
      - 404 Not Found: If the product does not exist.
      - 403 Forbidden: If the user is not the creator of the product.

    * To delete a specific product (return status):
      - 204 No Content: If the product is successfully deleted.
      - 404 Not Found: If the product does not exist.
      - 403 Forbidden: If the user is not the creator of the product.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            created_by=self.request.user).select_related('created_by').order_by("-id")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductReviewAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product reviews.

    This endpoint allows users to perform CRUD operations on product reviews.

    - List all reviews for a specific product and create a new review.
    - Retrieve, update, and delete a specific review.

    Responses:

    - GET request:
        - 200 OK: Returns a list of reviews for a specific product.

    - POST request:
        - 201 Created: Returns the created review.
        - 400 Bad Request: If the request data is invalid.

    - GET, PUT, PATCH, DELETE requests:
        - 404 Not Found: If the review or product does not exist.
        - 403 Forbidden: If the user is not the creator of the review.


    Examples:
    - To list all reviews for a specific product:
        ```http
        GET /products/{product_id}/reviews/
        ```

    - To create a new review for a specific product:
        ```http
        POST /products/{product_id}/reviews/
        ```
        Payload:
        ```json
        {
            "text": "Great product!",
            "rating": 5
        }
        ```

    - To retrieve a specific review:
        ```http
        GET /products/{product_id}/reviews/{review_id}/
        ```

    - To update a specific review:
        ```http
        PUT /products/{product_id}/reviews/{review_id}/
        ```
        Payload:
        ```json
        {
            "text": "Updated review text",
            "rating": 4
        }
        ```

    - To delete a specific review:
        ```http
        DELETE /products/{product_id}/reviews/{review_id}/
        ```
    Note:

    * To create a new review (return status):
      - 201 Created: If the review is successfully created.
      - 400 Bad Request: If the request data is invalid.

    * To update a specific review (return status).
      - 200 OK: If the review is successfully updated.
      - 404 Not Found: If the review or product does not exist.
      - 403 Forbidden: If the user is not the creator of the review.
      - 400 Bad Request: If the request data is invalid.

    * To retrieve a specific review (return status).
      - 200 OK: If the review is successfully retrieved.
      - 404 Not Found: If the review or product does not exist.
      - 403 Forbidden: If the user is not the creator of the review.

    * To delete a specific review (return status):
      - 204 No Content: If the review is successfully deleted.
      - 404 Not Found: If the review or product does not exist.
      - 403 Forbidden: If the user is not the creator of the review.
    """

    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs["product_id"]).select_related(
            'product', 'product__created_by', 'user').order_by('-id')

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs["product_id"], user=self.request.user)

