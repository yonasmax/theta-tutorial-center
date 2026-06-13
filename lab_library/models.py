from django.db import models
from students.models import Student
from datetime import date, timedelta

# ========== LABORATORY MODELS ==========

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('damaged', 'Damaged'),
    ]
    
    CATEGORY_CHOICES = [
        ('physics', 'Physics Equipment'),
        ('chemistry', 'Chemistry Equipment'),
        ('biology', 'Biology Equipment'),
        ('computer', 'Computer Lab'),
        ('general', 'General Equipment'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.available_quantity}/{self.quantity})"

class EquipmentBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='equipment_bookings')
    quantity = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purpose = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.equipment.name} ({self.status})"
    
    def is_overdue(self):
        if self.status != 'returned' and date.today() > self.expected_return_date:
            return True
        return False

class VirtualSimulation(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

# ========== LIBRARY MODELS ==========

class BookCategory(models.Model):
    CATEGORY_TYPES = [
        ('spiritual', 'Spiritual/Religious'),
        ('novel', 'Novel/Fiction'),
        ('educational', 'Educational'),
        ('reference', 'Reference'),
        ('children', 'Children\'s Books'),
    ]
    
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
    ]
    
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True, blank=True)
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, related_name='books')
    publication_year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class BookBorrowing(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='book_borrowings')
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')
    
    def __str__(self):
        return f"{self.student.name} - {self.book.title}"
    
    def is_overdue(self):
        if self.status == 'borrowed' and date.today() > self.due_date:
            return True
        return False