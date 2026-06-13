from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from datetime import date
from .models import (
    Equipment, EquipmentBooking, VirtualSimulation,
    BookCategory, Book, BookBorrowing
)
from .serializers import (
    EquipmentSerializer, EquipmentBookingSerializer, VirtualSimulationSerializer,
    BookCategorySerializer, BookSerializer, BookBorrowingSerializer
)

# Equipment Views
class EquipmentListView(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    
    def get_queryset(self):
        queryset = Equipment.objects.all()
        category = self.request.query_params.get('category', None)
        status = self.request.query_params.get('status', None)
        if category:
            queryset = queryset.filter(category=category)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class EquipmentBookingView(generics.ListCreateAPIView):
    queryset = EquipmentBooking.objects.all()
    serializer_class = EquipmentBookingSerializer

class EquipmentBookingDetailView(generics.RetrieveUpdateAPIView):
    queryset = EquipmentBooking.objects.all()
    serializer_class = EquipmentBookingSerializer

# Simulation Views
class VirtualSimulationListView(generics.ListAPIView):
    queryset = VirtualSimulation.objects.filter(is_active=True)
    serializer_class = VirtualSimulationSerializer

# Book Views
class BookCategoryListView(generics.ListAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        if category:
            queryset = queryset.filter(category__id=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(isbn__icontains=search)
            )
        return queryset

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookBorrowingView(generics.ListCreateAPIView):
    queryset = BookBorrowing.objects.all()
    serializer_class = BookBorrowingSerializer
    
    def get_queryset(self):
        queryset = BookBorrowing.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

class OverdueBooksView(APIView):
    def get(self, request):
        overdue = BookBorrowing.objects.filter(status='borrowed', due_date__lt=date.today())
        serializer = BookBorrowingSerializer(overdue, many=True)
        return Response({
            'count': overdue.count(),
            'overdue_items': serializer.data
        })

class AvailableBooksView(APIView):
    def get(self, request):
        available = Book.objects.filter(available_copies__gt=0, status='available')
        serializer = BookSerializer(available, many=True)
        return Response({
            'count': available.count(),
            'available_books': serializer.data
        })

# Dashboard View - ADD THIS AT THE BOTTOM
def lab_library_dashboard(request):
    return render(request, 'lab_library/dashboard.html')