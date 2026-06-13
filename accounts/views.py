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