from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from datetime import datetime, timedelta
from .models import Student, Lesson, StudentProgress, QuizScore, StudentActivity
from .serializers import StudentSerializer, LessonSerializer, StudentProgressSerializer
from lab_library.models import Book, Equipment
from finance.models import Payment

class MobileLoginView(APIView):
    """Mobile app login endpoint"""
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            student = Student.objects.get(name=username)
            
            import uuid
            token = f"mobile_token_{student.id}_{uuid.uuid4().hex[:16]}"
            
            return Response({
                'success': True,
                'token': token,
                'student_id': student.id,
                'name': student.name,
                'grade': student.grade,
                'email': student.email,
                'payment_status': student.payment_status,
                'message': 'Login successful'
            })
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

class MobileDashboardView(APIView):
    """Mobile app main dashboard"""
    
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            progress = StudentProgress.objects.filter(student=student)
            
            total_lessons = Lesson.objects.count()
            completed_lessons = progress.filter(status='completed').count()
            in_progress_lessons = progress.filter(status='in_progress').count()
            
            recent_progress = progress.order_by('-last_accessed')[:5]
            recent_lessons = []
            for p in recent_progress:
                recent_lessons.append({
                    'id': p.lesson.id,
                    'title': p.lesson.title,
                    'topic': p.lesson.topic,
                    'progress': p.progress_percentage,
                    'status': p.status
                })
            
            completed_ids = progress.filter(status='completed').values_list('lesson_id', flat=True)
            upcoming = Lesson.objects.exclude(id__in=completed_ids)[:5]
            upcoming_lessons = []
            for lesson in upcoming:
                upcoming_lessons.append({
                    'id': lesson.id,
                    'title': lesson.title,
                    'topic': lesson.topic,
                    'content_type': lesson.content_type
                })
            
            quiz_scores = QuizScore.objects.filter(student=student)
            avg_score = quiz_scores.aggregate(Sum('score'))['score__sum']
            avg_score = (avg_score / quiz_scores.count()) if quiz_scores.count() > 0 else 0
            
            payments = Payment.objects.filter(student=student)
            total_paid = payments.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
            
            return Response({
                'success': True,
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'grade': student.grade,
                    'payment_status': student.payment_status,
                },
                'stats': {
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons,
                    'in_progress_lessons': in_progress_lessons,
                    'completion_rate': round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0, 1),
                    'average_quiz_score': round(avg_score, 1),
                    'total_paid': float(total_paid),
                },
                'recent_lessons': recent_lessons,
                'upcoming_lessons': upcoming_lessons,
            })
        except Student.DoesNotExist:
            return Response({'success': False, 'message': 'Student not found'}, status=404)

class MobileLessonDetailView(APIView):
    """Get lesson details for mobile"""
    
    def get(self, request, student_id, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            student = Student.objects.get(id=student_id)
            
            progress = StudentProgress.objects.filter(student=student, lesson=lesson).first()
            
            quiz = QuizScore.objects.filter(student=student, lesson=lesson).first()
            
            return Response({
                'success': True,
                'lesson': {
                    'id': lesson.id,
                    'title': lesson.title,
                    'topic': lesson.topic,
                    'subject': lesson.subject.name if lesson.subject else None,
                    'grade': lesson.grade.level if lesson.grade else None,
                    'content_type': lesson.content_type,
                    'description': lesson.description,
                },
                'progress': {
                    'status': progress.status if progress else 'not_started',
                    'percentage': progress.progress_percentage if progress else 0,
                },
                'quiz_score': quiz.score if quiz else None,
            })
        except Lesson.DoesNotExist:
            return Response({'success': False, 'message': 'Lesson not found'}, status=404)

class MobileUpdateProgressView(APIView):
    """Update lesson progress from mobile"""
    
    def post(self, request):
        student_id = request.data.get('student_id')
        lesson_id = request.data.get('lesson_id')
        progress_percentage = request.data.get('progress_percentage', 0)
        
        try:
            progress, created = StudentProgress.objects.get_or_create(
                student_id=student_id,
                lesson_id=lesson_id
            )
            
            progress.progress_percentage = progress_percentage
            if progress_percentage >= 100:
                progress.status = 'completed'
            elif progress_percentage > 0:
                progress.status = 'in_progress'
            
            progress.save()
            
            StudentActivity.objects.create(
                student_id=student_id,
                activity_type='view_lesson',
                details=f"Progress updated to {progress_percentage}%"
            )
            
            return Response({'success': True, 'progress': progress_percentage})
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

class MobileLibraryView(APIView):
    """Get library books for mobile"""
    
    def get(self, request):
        category = request.query_params.get('category', None)
        books = Book.objects.all()
        if category:
            books = books.filter(category__category_type=category)
        
        book_list = []
        for book in books[:20]:
            book_list.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'category': book.category.name if book.category else None,
                'available_copies': book.available_copies,
                'total_copies': book.total_copies,
                'status': book.status,
            })
        
        return Response({'success': True, 'books': book_list})

class MobileEquipmentView(APIView):
    """Get lab equipment for mobile"""
    
    def get(self, request):
        equipment = Equipment.objects.all()
        equipment_list = []
        for eq in equipment[:20]:
            equipment_list.append({
                'id': eq.id,
                'name': eq.name,
                'category': eq.category,
                'available': eq.available_quantity,
                'total': eq.quantity,
                'status': eq.status,
            })
        
        return Response({'success': True, 'equipment': equipment_list})

class MobileNotificationsView(APIView):
    """Get student notifications"""
    
    def get(self, request, student_id):
        notifications = []
        
        from lab_library.models import BookBorrowing
        overdue = BookBorrowing.objects.filter(
            student_id=student_id,
            status='borrowed',
            due_date__lt=datetime.now().date()
        )
        for book in overdue:
            notifications.append({
                'type': 'overdue_book',
                'title': 'Book Overdue',
                'message': f"'{book.book.title}' is overdue. Please return it.",
                'date': book.due_date.isoformat(),
            })
        
        from finance.models import Invoice
        unpaid = Invoice.objects.filter(student_id=student_id, is_paid=False)
        for invoice in unpaid:
            if invoice.due_date < datetime.now().date():
                notifications.append({
                    'type': 'payment_due',
                    'title': 'Payment Due',
                    'message': f"Invoice {invoice.invoice_number} of {invoice.amount} ETB is due.",
                    'date': invoice.due_date.isoformat(),
                })
        
        from .models import Certificate
        certificates = Certificate.objects.filter(student_id=student_id)[:3]
        for cert in certificates:
            notifications.append({
                'type': 'certificate',
                'title': 'New Certificate!',
                'message': f"You earned a certificate for {cert.get_certificate_type_display()}",
                'date': cert.issued_date.isoformat(),
            })
        
        return Response({
            'success': True,
            'notifications': notifications,
            'unread_count': len(notifications)
        })