from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import throttling, permissions
from rest_framework.views import APIView, View
from .serializer import TransactionSerializer
from .models import Transaction
from django.core.cache import cache
from rest_framework import status
from django.db.models import Sum
from asgiref.sync import sync_to_async
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

class StrictThrottle(throttling.UserRateThrottle):
    scope = "user"

# Paginated Transaction
class TransactionListView(APIView):
    throttle_classes = [StrictThrottle]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user).order_by("-timestamp")
        paginator = PageNumberPagination()
        paginator.page_size = 1
        result = paginator.paginate_queryset(queryset, request)
        serializer = TransactionSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            cache.delete(f"pnl_summary_{request.user.id}")  # invalidate cache
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Async P&L Summary
class PnLSummaryView(View):
    permission_classes = [permissions.IsAuthenticated]

    async def get(self, request):
        # Manually authenticate using JWT
        user = None
        try:
            jwt_auth = JWTAuthentication()
            validated = await sync_to_async(jwt_auth.authenticate)(request)
            if validated is not None:
                user, _ = validated
        except Exception:
            user = None

        if not user or not user.is_authenticated:
            return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)

        request.user = user  # set user for rest of view
        
        cache_key = f"pnl_summary_{request.user.id}"
        cached_data = await sync_to_async(cache.get)(cache_key)
        if(cached_data):
            return JsonResponse(cached_data, status=200)
        
        income = await sync_to_async(
            lambda: Transaction.objects.filter(user=request.user, type="INCOME").aggregate(total=Sum("amount"))["total"] or 0
        )()

        expense = await sync_to_async(
            lambda: Transaction.objects.filter(user=request.user, type="EXPENSE").aggregate(total=Sum("amount"))["total"] or 0
        )()

        pnl_summary = {
            "income": income,
            "expense": expense,
            "pnl": income - expense
        }

        await sync_to_async(cache.set)(cache_key, pnl_summary, timeout=60)  # cache for 1 minute
        return JsonResponse(pnl_summary, status=200)
