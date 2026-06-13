from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    GRADE_CHOICES = [
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    
    PAYMENT_CHOICES = [
        ('Paid', 'Paid ✓'),
        ('Not Paid', 'Not Paid ✗'),
    ]
    
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Not Paid')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.grade}"

class Subject(models.Model):
    GRADE_CHOICES = [
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.grade})"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.student.name} - ${self.amount} - {'Paid' if self.is_paid else 'Not Paid'}"
class Subject(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.level

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    content_type = models.CharField(
        max_length=20,
        choices=[('video', 'Video'), ('quiz', 'Quiz'), ('article', 'Article')]
    )
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
class Grade(models.Model):
    level = models.CharField(max_length=50)  # e.g., "Grade 10", "Grade 11"
    
    def __str__(self):
        return self.level

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='lessons')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name='lessons')
    content_type = models.CharField(
        max_length=20,
        choices=[('video', 'Video'), ('quiz', 'Quiz'), ('article', 'Article')]
    )
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title