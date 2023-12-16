from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import _get_queryset
import jwt
from rest_framework import exceptions


class StockInsufficient(Exception):
    pass


class OrderException(Exception):
    pass


class OrderExceptionMixin:
    def handle_exception(self, exc):
        if isinstance(exc, (StockInsufficient, OrderException)):
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class JWTExceptionMixin:
    def handle_exception(self, exc):
        if isinstance(exc, (jwt.ExpiredSignatureError, jwt.DecodeError)):
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class PermissionExceptionMixin:
    def handle_exception(self, exc):
        if isinstance(exc, exceptions.PermissionDenied):
            return Response({'detail': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)


class NotFoundExceptionMixin:
    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

    def get_object_or_404(self, *args, **kwargs):
        return self.get_object_or_404_from_queryset(self.get_queryset(), *args, **kwargs)

    @staticmethod
    def get_object_or_404_from_queryset(klass, *args, **kwargs):
        """
        Use get() to return an object, or raise a Http404 exception if the object
        does not exist.

        klass may be a Model, Manager, or QuerySet object. All other passed
        arguments and keyword arguments are used in the get() query.

        Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
        one object is found.
        """
        error = kwargs.pop("error", None)
        queryset = _get_queryset(klass)
        if not hasattr(queryset, 'get'):
            klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            raise ValueError(
                "First argument to get_object_or_404() must be a Model, Manager, "
                "or QuerySet, not '%s'." % klass__name
            )
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % queryset.model._meta.object_name if not error else error)
