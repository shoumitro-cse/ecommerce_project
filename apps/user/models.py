from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Attributes:
        profile_photo (ImageField, optional): An image representing the user's profile (can be blank or null).

    Additional fields and methods are inherited from AbstractUser.

    Example:
        >>> user = User(username='john_doe', email='john@example.com', profile_photo='path/to/photo.jpg')
        >>> user.save()
    """

    profile_photo = models.ImageField(upload_to='user/profile/', blank=True, null=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
