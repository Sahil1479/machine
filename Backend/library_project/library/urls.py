from django.urls import path

from .views import BookListAPIView, BookDetailAPIView, AsyncSearchBooksAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/search/', AsyncSearchBooksAPIView.as_view(), name='book-search'),
]