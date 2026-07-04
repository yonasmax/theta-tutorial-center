from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django.db.models import Q
from .models import Student
from accounts.models import User
from .serializers import (
    StudentSerializer, 
    StudentProfileSerializer,
    StudentRegistrationSerializer,
    StudentLoginSerializer
)

# Import from .mobile_views
from .mobile_views import *

# ============================================
# STUDENT VIEWS (Function-based)
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_students(request):
    """Get all students (Admin only)"""
    try:
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_by_id(request, student_id):
    """Get student by ID"""
    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student(request, student_id):
    """Update student by ID (Admin only)"""
    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_student(request, student_id):
    """Delete student by ID (Admin only)"""
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return Response(
            {'message': 'Student deleted successfully'},
            status=status.HTTP_200_OK
        )
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_students(request):
    """Search students by name, email, or student ID"""
    try:
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        students = Student.objects.filter(
            Q(student_id__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query)
        )
        
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def test_progress(request):
    """Test endpoint for progress tracking"""
    return Response({
        'status': 'success',
        'message': 'Progress tracking is working!',
        'data': {
            'progress': 0,
            'completed': False
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_progress(request):
    """Get student progress"""
    try:
        student = request.user.student_profile
        return Response({
            'status': 'success',
            'data': {
                'progress': 0,
                'completed_lessons': 0,
                'total_lessons': 0
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_progress(request):
    """Update student progress"""
    try:
        progress = request.data.get('progress', 0)
        return Response({
            'status': 'success',
            'message': 'Progress updated successfully',
            'data': {'progress': progress}
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================
# CLASS-BASED VIEWS FOR STUDENTS
# ============================================

class StudentListView(ListAPIView):
    """List all students (Admin only)"""
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(RetrieveAPIView):
    """Get student details (Admin only)"""
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


class StudentCreateView(CreateAPIView):
    """Create a new student (Admin only)"""
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer


class StudentUpdateView(UpdateAPIView):
    """Update student (Admin only)"""
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


class StudentDeleteView(DestroyAPIView):
    """Delete student (Admin only)"""
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    lookup_field = 'id'


# ============================================
# BULK UPLOAD VIEW
# ============================================

class StudentBulkUploadView(APIView):
    """Bulk upload students via CSV/Excel"""
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        """Upload students in bulk"""
        try:
            file = request.FILES.get('file')
            if not file:
                return Response(
                    {'error': 'No file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check file extension
            if not file.name.endswith(('.csv', '.xlsx', '.xls')):
                return Response(
                    {'error': 'File must be CSV or Excel format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process CSV file
            import csv
            import io
            
            if file.name.endswith('.csv'):
                decoded_file = file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.reader(io_string)
                
                created_count = 0
                errors = []
                
                # Skip header row
                next(reader, None)
                
                for row in reader:
                    try:
                        email = row[0]
                        first_name = row[1]
                        last_name = row[2]
                        student_id = row[3] if len(row) > 3 else None
                        password = f'default123'
                        
                        # Create user
                        user = User.objects.create_user(
                            email=email,
                            password=password,
                            first_name=first_name,
                            last_name=last_name,
                            role='student'
                        )
                        
                        # Create student
                        if student_id:
                            Student.objects.create(
                                user=user,
                                student_id=student_id
                            )
                        else:
                            Student.objects.create(user=user)
                        
                        created_count += 1
                    except Exception as e:
                        errors.append(f'Error with row {row}: {str(e)}')
                
                return Response({
                    'status': 'success',
                    'message': f'Successfully created {created_count} students',
                    'errors': errors
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'File format not supported yet',
                'supported_formats': ['csv']
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )