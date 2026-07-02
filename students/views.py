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
from .models import Student, Subject, Lesson, Grade, StudentProgress, QuizScore, StudentActivity, Certificate, Note
from .models import Quiz, Question, Choice, QuizAttempt, StudentAnswer
from .serializers import (
    LessonSerializer, StudentSerializer, SubjectSerializer, 
    StudentProgressSerializer, QuizScoreSerializer, CertificateSerializer,
    QuizSerializer, QuizAttemptSerializer, NoteSerializer
)

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

# ========== STUDENT MANAGEMENT VIEWS ==========

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific student"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentCreateView(generics.CreateAPIView):
    """Create a new student"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentBulkUploadView(APIView):
    """Bulk upload students via JSON"""
    def post(self, request):
        students_data = request.data.get('students', [])
        created_count = 0
        errors = []
        
        for data in students_data:
            try:
                student = Student.objects.create(
                    name=data.get('name'),
                    grade=data.get('grade'),
                    email=data.get('email', ''),
                    phone=data.get('phone', ''),
                    payment_status=data.get('payment_status', 'Not Paid')
                )
                created_count += 1
            except Exception as e:
                errors.append(str(e))
        
        return Response({
            'message': f'Created {created_count} students',
            'errors': errors
        })

class StudentStatsView(APIView):
    """Get statistics about students"""
    def get(self, request):
        total = Student.objects.count()
        by_grade = {}
        by_payment = {}
        
        for grade in ['9', '10', '11', '12']:
            by_grade[f'Grade {grade}'] = Student.objects.filter(grade=grade).count()
        
        by_payment['Paid'] = Student.objects.filter(payment_status='Paid').count()
        by_payment['Not Paid'] = Student.objects.filter(payment_status='Not Paid').count()
        
        return Response({
            'total_students': total,
            'by_grade': by_grade,
            'by_payment_status': by_payment,
        })

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
            return Response({'message': f'Certificate email sent to {certificate.student.email}'})
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found'}, status=404)

class SendProgressReportView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        
        try:
            student = Student.objects.get(id=student_id)
            return Response({'message': f'Progress report sent to {student.email}'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

# ========== QUIZ SYSTEM VIEWS ==========

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizSerializer

class LessonQuizView(APIView):
    def get(self, request, lesson_id):
        try:
            quiz = Quiz.objects.get(lesson_id=lesson_id, is_active=True)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response({'error': 'No quiz available for this lesson'}, status=404)

class StartQuizView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        quiz_id = request.data.get('quiz_id')
        
        existing_attempt = QuizAttempt.objects.filter(
            student_id=student_id, 
            quiz_id=quiz_id, 
            completed_at__isnull=True
        ).first()
        
        if existing_attempt:
            return Response({
                'attempt_id': existing_attempt.id,
                'message': 'Continuing existing attempt'
            })
        
        attempt = QuizAttempt.objects.create(
            student_id=student_id,
            quiz_id=quiz_id
        )
        
        return Response({
            'attempt_id': attempt.id,
            'message': 'Quiz started successfully'
        })

class SubmitQuizView(APIView):
    def post(self, request):
        attempt_id = request.data.get('attempt_id')
        answers = request.data.get('answers', [])
        
        try:
            attempt = QuizAttempt.objects.get(id=attempt_id)
            quiz = attempt.quiz
            total_points = 0
            earned_points = 0
            
            for answer_data in answers:
                question_id = answer_data.get('question_id')
                choice_id = answer_data.get('choice_id')
                answer_text = answer_data.get('answer_text', '')
                
                question = Question.objects.get(id=question_id)
                total_points += question.points
                
                is_correct = False
                points_earned = 0
                
                if question.question_type in ['multiple_choice', 'true_false'] and choice_id:
                    choice = Choice.objects.get(id=choice_id)
                    is_correct = choice.is_correct
                    if is_correct:
                        points_earned = question.points
                        earned_points += points_earned
                    
                    StudentAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_choice=choice,
                        is_correct=is_correct,
                        points_earned=points_earned
                    )
                elif question.question_type == 'short_answer':
                    correct_answer = question.choices.filter(is_correct=True).first()
                    if correct_answer and answer_text.lower().strip() == correct_answer.choice_text.lower().strip():
                        is_correct = True
                        points_earned = question.points
                        earned_points += points_earned
                    
                    StudentAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        answer_text=answer_text,
                        is_correct=is_correct,
                        points_earned=points_earned
                    )
            
            percentage = int((earned_points / total_points) * 100) if total_points > 0 else 0
            passed = percentage >= quiz.passing_score
            
            attempt.score = earned_points
            attempt.total_points = total_points
            attempt.percentage = percentage
            attempt.passed = passed
            attempt.completed_at = timezone.now()
            attempt.save()
            
            if passed:
                progress, _ = StudentProgress.objects.get_or_create(
                    student_id=attempt.student_id,
                    lesson_id=quiz.lesson_id
                )
                if progress.progress_percentage < 100:
                    progress.progress_percentage = 100
                    progress.status = 'completed'
                    progress.completed_at = timezone.now()
                    progress.save()
            
            return Response({
                'attempt_id': attempt.id,
                'score': earned_points,
                'total_points': total_points,
                'percentage': percentage,
                'passed': passed,
                'message': 'Quiz submitted successfully!'
            })
        except QuizAttempt.DoesNotExist:
            return Response({'error': 'Attempt not found'}, status=404)

class QuizResultView(APIView):
    def get(self, request, attempt_id):
        try:
            attempt = QuizAttempt.objects.get(id=attempt_id)
            serializer = QuizAttemptSerializer(attempt)
            
            answers = StudentAnswer.objects.filter(attempt=attempt)
            answers_data = []
            for answer in answers:
                answers_data.append({
                    'question_id': answer.question.id,
                    'question_text': answer.question.question_text,
                    'is_correct': answer.is_correct,
                    'points_earned': answer.points_earned,
                    'selected_choice': answer.selected_choice.choice_text if answer.selected_choice else None,
                    'correct_answer': answer.question.choices.filter(is_correct=True).first().choice_text if answer.question.choices.filter(is_correct=True).exists() else None
                })
            
            return Response({
                'attempt': serializer.data,
                'answers': answers_data
            })
        except QuizAttempt.DoesNotExist:
            return Response({'error': 'Attempt not found'}, status=404)

# ========== NOTES VIEWS ==========

class NoteListView(generics.ListAPIView):
    """List all notes with filtering"""
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        queryset = Note.objects.filter(is_published=True)
        
        grade = self.request.query_params.get('grade', None)
        if grade:
            queryset = queryset.filter(grade=grade)
        
        subject = self.request.query_params.get('subject', None)
        if subject:
            queryset = queryset.filter(subject=subject)
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(topic__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset

class NoteDetailView(generics.RetrieveAPIView):
    """Get single note with view count increment"""
    queryset = Note.objects.filter(is_published=True)
    serializer_class = NoteSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class NoteCreateView(generics.CreateAPIView):
    """Create a new note"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteUpdateView(generics.UpdateAPIView):
    """Update a note"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteDeleteView(generics.DestroyAPIView):
    """Delete a note"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteStatsView(APIView):
    """Get statistics about notes"""
    def get(self, request):
        total = Note.objects.filter(is_published=True).count()
        by_grade = {}
        by_subject = {}
        
        for grade in ['9', '10', '11', '12']:
            by_grade[f'Grade {grade}'] = Note.objects.filter(grade=grade, is_published=True).count()
        
        for subject in ['mathematics', 'physics', 'chemistry', 'biology', 'history', 'geography', 'english', 'amharic']:
            by_subject[subject] = Note.objects.filter(subject=subject, is_published=True).count()
        
        return Response({
            'total_notes': total,
            'by_grade': by_grade,
            'by_subject': by_subject,
        })

# ========== GRADE 10 SPECIFIC VIEWS ==========

class Grade10DashboardView(APIView):
    """Get Grade 10 student dashboard data"""
    
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id, grade='10')
            lessons = Lesson.objects.filter(grade__level='Grade 10')
            progress = StudentProgress.objects.filter(student=student)
            
            total_lessons = lessons.count()
            completed_lessons = progress.filter(status='completed').count()
            in_progress_lessons = progress.filter(status='in_progress').count()
            
            subjects = Subject.objects.filter(grade='10')
            notes = Note.objects.filter(grade='10', is_published=True)[:5]
            quizzes = Quiz.objects.filter(lesson__grade__level='Grade 10', is_active=True)[:5]
            
            return Response({
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'grade': student.grade,
                    'profile_picture': student.profile_picture.url if student.profile_picture else None,
                },
                'stats': {
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons,
                    'in_progress_lessons': in_progress_lessons,
                    'completion_rate': round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0, 1),
                },
                'subjects': [{'name': s.name, 'id': s.id} for s in subjects],
                'recent_notes': NoteSerializer(notes, many=True).data,
                'available_quizzes': QuizSerializer(quizzes, many=True).data,
            })
        except Student.DoesNotExist:
            return Response({'error': 'Student not found or not in Grade 10'}, status=404)

class Grade10SubjectsView(generics.ListAPIView):
    """Get all subjects for Grade 10"""
    serializer_class = SubjectSerializer
    
    def get_queryset(self):
        return Subject.objects.filter(grade='10')

class Grade10LessonsView(generics.ListAPIView):
    """Get all lessons for Grade 10"""
    serializer_class = LessonSerializer
    
    def get_queryset(self):
        return Lesson.objects.filter(grade__level='Grade 10')

class Grade10NotesView(generics.ListAPIView):
    """Get all notes for Grade 10"""
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        queryset = Note.objects.filter(grade='10', is_published=True)
        subject = self.request.query_params.get('subject', None)
        if subject:
            queryset = queryset.filter(subject=subject)
        return queryset

class Grade10QuizzesView(generics.ListAPIView):
    """Get all quizzes for Grade 10"""
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        return Quiz.objects.filter(lesson__grade__level='Grade 10', is_active=True)