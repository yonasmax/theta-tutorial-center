from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.finance_dashboard, name='finance_dashboard'),  # ADD THIS LINE
    path('payment-methods/', views.PaymentMethodListView.as_view(), name='payment-methods'),
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscriptions'),
    path('payments/', views.PaymentListView.as_view(), name='payments'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoices'),
    path('balance/<int:student_id>/', views.StudentBalanceView.as_view(), name='student-balance'),
]