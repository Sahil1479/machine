from django.urls import path
from .views import TransactionListView, PnLSummaryView

urlpatterns = [
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("pnl/", PnLSummaryView.as_view(), name="pnl-summary"),
]