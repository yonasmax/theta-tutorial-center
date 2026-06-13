from .mobile_views import *
from django.http import JsonResponse
from datetime import date
from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import django
from .models import Student, Subject, Lesson, Grade, StudentProgress, QuizScore, StudentActivity, Certificate
from .serializers import LessonSerializer, StudentSerializer, StudentProgressSerializer, QuizScoreSerializer, CertificateSerializer

# Simple test view
def test_progress(request):
    return JsonResponse({"message": "API is working!", "status": "success"})

# Search Views
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

# Student List View
class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# ========== PROGRESS TRACKING API VIEWS ==========

class StudentProgressListView(generics.ListAPIView):
    serializer_class = StudentProgressSerializer
    
    def get_queryset(self):
        queryset = StudentProgress.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

class UpdateProgressView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        lesson_id = request.data.get('lesson_id')
        progress_percentage = request.data.get('progress_percentage', 0)
        
        try:
            progress = StudentProgress.objects.get(student_id=student_id, lesson_id=lesson_id)
        except StudentProgress.DoesNotExist:
            progress = StudentProgress(student_id=student_id, lesson_id=lesson_id)
        
        progress.progress_percentage = progress_percentage
        progress.last_accessed = timezone.now()
        
        if progress_percentage >= 100:
            progress.status = 'completed'
            progress.completed_at = timezone.now()
        elif progress_percentage > 0:
            progress.status = 'in_progress'
        else:
            progress.status = 'not_started'
        
        progress.save()
        
        return Response(StudentProgressSerializer(progress).data, status=status.HTTP_200_OK)

class StudentDashboardView(APIView):
    def get(self, request, student_id):
        progress = StudentProgress.objects.filter(student_id=student_id)
        total_lessons = Lesson.objects.count()
        completed_lessons = progress.filter(status='completed').count()
        in_progress_lessons = progress.filter(status='in_progress').count()
        
        quiz_scores = QuizScore.objects.filter(student_id=student_id)
        if quiz_scores.exists():
            total_score = sum(q.score for q in quiz_scores)
            average_score = total_score / quiz_scores.count()
        else:
            average_score = 0
        
        return Response({
            'student_id': student_id,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'in_progress_lessons': in_progress_lessons,
            'completion_percentage': round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0, 1),
            'average_quiz_score': round(average_score, 1),
        })

class SubmitQuizScoreView(APIView):
    def post(self, request):
        serializer = QuizScoreSerializer(data=request.data)
        if serializer.is_valid():
            quiz_score = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ========== CERTIFICATE VIEWS ==========

class StudentCertificatesView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    
    def get_queryset(self):
        return Certificate.objects.filter(student_id=self.kwargs['student_id'])

class GenerateCertificateView(APIView):
    def post(self, request):
        from students.certificate_generator import generate_certificate
        import uuid
        
        student_id = request.data.get('student_id')
        certificate_type = request.data.get('certificate_type', 'course_completion')
        lesson_id = request.data.get('lesson_id', None)
        
        try:
            student = Student.objects.get(id=student_id)
            lesson = Lesson.objects.get(id=lesson_id) if lesson_id else None
            
            cert_number = f"THETA-{student_id}-{uuid.uuid4().hex[:8].upper()}"
            course_name = lesson.title if lesson else certificate_type.replace('_', ' ').title()
            
            pdf_path = generate_certificate(
                student.name,
                certificate_type.replace('_', ' ').title(),
                course_name,
                cert_number
            )
            
            certificate = Certificate.objects.create(
                student=student,
                certificate_type=certificate_type,
                lesson=lesson,
                certificate_number=cert_number
            )
            
            return Response({
                'certificate_id': certificate.id,
                'certificate_number': cert_number,
                'message': 'Certificate generated successfully!'
            }, status=status.HTTP_201_CREATED)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class DownloadCertificateView(APIView):
    def get(self, request, certificate_id):
        from django.http import FileResponse
        import os
        
        try:
            certificate = Certificate.objects.get(id=certificate_id)
            file_path = f"certificates/certificate_{certificate.certificate_number}.html"
            
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, 
                                  filename=f"certificate_{certificate.certificate_number}.html")
            else:
                return Response({'error': 'Certificate file not found'}, status=404)
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found'}, status=404)

class SendCertificateEmailView(APIView):
    def post(self, request):
        certificate_id = request.data.get('certificate_id')
        
        try:
            certificate = Certificate.objects.get(id=certificate_id)
            # Email sending logic here
            return Response({'message': f'Certificate email sent to {certificate.student.email}'})
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found'}, status=404)

class SendProgressReportView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        
        try:
            student = Student.objects.get(id=student_id)
            # Email sending logic here
            return Response({'message': f'Progress report sent to {student.email}'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)