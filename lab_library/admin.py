from django.contrib import admin
from .models import (
    Equipment, EquipmentBooking, VirtualSimulation,
    BookCategory, Book, BookBorrowing
)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'available_quantity', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name',)

@admin.register(EquipmentBooking)
class EquipmentBookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'equipment', 'quantity', 'status', 'expected_return_date')
    list_filter = ('status',)

@admin.register(VirtualSimulation)
class VirtualSimulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'is_active')

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_copies', 'available_copies')
    list_filter = ('category', 'status')
    search_fields = ('title', 'author', 'isbn')

@admin.register(BookBorrowing)
class BookBorrowingAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'due_date', 'status')
    list_filter = ('status',)