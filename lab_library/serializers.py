from rest_framework import serializers
from .models import (
    Equipment, EquipmentBooking, VirtualSimulation,
    BookCategory, Book, BookBorrowing
)

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class EquipmentBookingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    
    class Meta:
        model = EquipmentBooking
        fields = '__all__'

class VirtualSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualSimulation
        fields = '__all__'

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'

class BookBorrowingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = BookBorrowing
        fields = '__all__'