# Custom throttles
class BurstThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedThrottle(UserRateThrottle):
    scope = 'sustained'

# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

# Book API
class BookListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_throttles(self):
        if self.request.method == "GET":
            return [BurstThrottle()]
        return [SustainedThrottle()]
    
    def get(self, request):
        cached_books = cache.get("book_list")
        if cached_books:
            return Response(cached_books)
        
        books = Books.objects.select_related("author").all()
        # custom pagination object
        paginator = PageNumberPagination()
        paginator.page_size = 3  # override default PAGE_SIZE here if needed

        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)

        cache.set("book_list", serializer.data, timeout=60)
        return paginator.get_paginated_response(serializer.data)
    
    '''
        Sample API Response

        GET /books/?page=2

        {
            "count": 12,
            "next": "http://127.0.0.1:8000/books/?page=3",
            "previous": "http://127.0.0.1:8000/books/?page=1",
            "results": [
                {
                    "id": 4,
                    "title": "Book 4",
                    "author": "Author X",
                    "published_year": 2018
                },
                {
                    "id": 5,
                    "title": "Book 5",
                    "author": "Author Y",
                    "published_year": 2019
                },
                {
                    "id": 6,
                    "title": "Book 6",
                    "author": "Author Z",
                    "published_year": 2020
                }
            ]
        }
    '''
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    # Default fallback
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return [permissions.AllowAny()]
        elif(self.request.method in ['POST', 'PUT', 'PATCH']):
            return [permissions.IsAuthenticated()]
        elif(self.request.method == 'DELETE'):
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book.created_by != request.user:
            return Response({"error": "Not your book!"}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book.created_by != request.user:
            return Response({"error": "Not your book!"}, status=status.HTTP_403_FORBIDDEN)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Async Example (search books)
class AsyncSearchBooksAPIView(APIView):
    async def get(self, request):
        query = request.query_params.get("q", "")
        books = await sync_to_async(list)(Book.objects.filter(title__icontains=query))
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)