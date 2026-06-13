from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from students.models import Student, Subject, Lesson, Grade
from .serializers import LessonSerializer

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'accounts/login.html')

@login_required
def student_dashboard(request):
    students = Student.objects.filter(name=request.user.username)
    if students.exists():
        student = students.first()
        subjects = Subject.objects.filter(grade=student.grade)
        context = {
            'student': student,
            'grade': student.grade,
            'subjects': subjects,
            'payment_status': student.payment_status,
        }
    else:
        context = {
            'student': None,
            'grade': 'Not Found',
            'subjects': [],
            'payment_status': 'Not Registered',
        }
    return render(request, 'accounts/dashboard.html', context)

def student_logout(request):
    logout(request)
    return redirect('student_login')

class LessonSearchView(generics.ListAPIView):
    serializer_class = LessonSerializer
    def get_queryset(self):
        queryset = Lesson.objects.all()
        search_query = self.request.query_params.get('search', None)
        grade = self.request.query_params.get('grade', None)
        subject = self.request.query_params.get('subject', None)
        content_type = self.request.query_params.get('content_type', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(topic__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        if grade:
            queryset = queryset.filter(grade__level=grade)
        if subject:
            queryset = queryset.filter(subject__name=subject)
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        return queryset

class FilterOptionsView(APIView):
    def get(self, request):
        grades = Grade.objects.values_list('level', flat=True).distinct()
        subjects = Subject.objects.values_list('name', flat=True).distinct()
        content_types = ['video', 'quiz', 'article']
        return Response({
            'grades': grades,
            'subjects': subjects,
            'content_types': content_types,
        })

def search_page(request):
    return render(request, 'accounts/search.html')
def dashboard_page(request):
    return render(request, 'accounts/dashboard.html')
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def student_login_page(request):
    return render(request, 'accounts/student_login.html')

def student_login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to find student by name
        try:
            student = Student.objects.get(name=username)
            # Simple authentication - you can enhance this
            if password == student.id or password == student.grade:
                # Create or get user for Django auth
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'password': 'pbkdf2_sha256$dummy'}
                )
                login(request, user)
                request.session['student_id'] = student.id
                return redirect('student_portal')
            else:
                messages.error(request, 'Invalid student ID or credentials')
        except Student.DoesNotExist:
            messages.error(request, 'Student not found')
    
    return redirect('student_login_page')

def student_portal(request):
    if not request.user.is_authenticated:
        return redirect('student_login_page')
    
    student_id = request.session.get('student_id')
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('student_login_page')
    
    # Get student's lessons with progress
    from students.models import Lesson, StudentProgress
    all_lessons = Lesson.objects.filter(grade__level=f"Grade {student.grade}")
    lessons_with_progress = []
    completed = 0
    
    for lesson in all_lessons:
        progress = StudentProgress.objects.filter(student=student, lesson=lesson).first()
        progress_percent = progress.progress_percentage if progress else 0
        if progress_percent >= 100:
            completed += 1
        lessons_with_progress.append({
            'id': lesson.id,
            'title': lesson.title,
            'topic': lesson.topic,
            'progress': progress_percent,
        })
    
    total = all_lessons.count()
    completion_rate = round((completed / total * 100) if total > 0 else 0)
    
    context = {
        'student': student,
        'lessons': lessons_with_progress,
        'total_lessons': total,
        'completed_lessons': completed,
        'completion_rate': completion_rate,
        'payment_status': student.payment_status,
    }
    return render(request, 'accounts/student_portal.html', context)

def student_logout_action(request):
    logout(request)
    return redirect('student_login_page')
# ========== QUIZ UI VIEWS ==========

def quiz_list(request):
    if not request.user.is_authenticated:
        return redirect('student_login_page')
    return render(request, 'accounts/quiz_list.html')

def take_quiz(request, quiz_id):
    if not request.user.is_authenticated:
        return redirect('student_login_page')
    
    student_id = request.session.get('student_id')
    context = {
        'student_id': student_id,
        'quiz_id': quiz_id
    }
    return render(request, 'accounts/take_quiz.html', context)