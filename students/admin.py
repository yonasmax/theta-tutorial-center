from django.contrib import admin
from .models import Student, Subject, Fee, Grade, Lesson

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'payment_status', 'registered_date')
    list_filter = ('grade', 'payment_status')
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade')
    list_filter = ('grade',)
    search_fields = ('name',)

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'is_paid', 'payment_date')
    list_filter = ('is_paid', 'payment_date')
    search_fields = ('student__name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('level',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'subject', 'grade', 'content_type')
    list_filter = ('subject', 'grade', 'content_type')
    search_fields = ('title', 'topic', 'description')