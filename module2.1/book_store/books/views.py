from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Author, Book
from books.serializers import AuthorSerializer, BookSerializer, BookBuySerializer


class AuthorViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["post"], serializer_class=BookBuySerializer)
    def buy(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            get_object_or_404(Book, id=pk)
        except Book.DoesNotExist:
            return Response({"detail": "The book does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            Book.objects.filter(id=pk).update(count=F('count') - serializer.validated_data["count"])
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except IntegrityError:
            return Response({"detail": "Not enough books."},
                            status=status.HTTP_400_BAD_REQUEST)
