from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.lab_library_dashboard, name='lab_library_dashboard'),
    path('equipment/', views.EquipmentListView.as_view(), name='equipment-list'),
    path('equipment-bookings/', views.EquipmentBookingView.as_view(), name='equipment-bookings'),
    path('equipment-bookings/<int:pk>/', views.EquipmentBookingDetailView.as_view(), name='equipment-booking-detail'),
    
    # Simulation URLs
    path('simulations/', views.VirtualSimulationListView.as_view(), name='simulations'),
    
    # Book URLs
    path('book-categories/', views.BookCategoryListView.as_view(), name='book-categories'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book-borrowings/', views.BookBorrowingView.as_view(), name='book-borrowings'),
    path('overdue-books/', views.OverdueBooksView.as_view(), name='overdue-books'),
    path('available-books/', views.AvailableBooksView.as_view(), name='available-books'),
]