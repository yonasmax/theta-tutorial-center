from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from .models import PaymentMethod, Subscription, Payment, Invoice
from .serializers import (
    PaymentMethodSerializer, SubscriptionSerializer, 
    PaymentSerializer, InvoiceSerializer
)

class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer

class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        queryset = Subscription.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    
    def get_queryset(self):
        queryset = Invoice.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

class StudentBalanceView(APIView):
    def get(self, request, student_id):
        total_paid = Payment.objects.filter(student_id=student_id, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = Invoice.objects.filter(student_id=student_id, is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'student_id': student_id,
            'total_paid': total_paid,
            'total_due': total_due,
            'balance': total_due - total_paid
        })

# Add this function at the bottom
def finance_dashboard(request):
    return render(request, 'finance/dashboard.html')