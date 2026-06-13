from django.db import models
from students.models import Student

class PaymentMethod(models.Model):
    METHOD_CHOICES = [
        ('telebirr', 'TeleBirr'),
        ('cbe', 'CBE Birr'),
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
    ]
    
    name = models.CharField(max_length=20, choices=METHOD_CHOICES)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.get_name_display()

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly - 500 ETB'),
        ('quarterly', 'Quarterly - 1,350 ETB'),
        ('yearly', 'Yearly - 5,000 ETB'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    def __str__(self):
        return f"{self.student.name} - {self.get_plan_display()}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.amount} ETB - {self.status}"

class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.student.name}"