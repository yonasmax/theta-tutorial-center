from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json

# Import from library instead of labresources
from library.models import Book, Equipment  # 👈 UPDATED

from .models import Student
from .serializers import StudentSerializer, StudentProfileSerializer
from accounts.models import User

# ============================================
# STUDENT REGISTRATION & AUTHENTICATION
# ============================================

@api_view(['POST'])
@permission_classes([AllowAny])
def student_register(request):
    """Student registration endpoint"""
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        student_id = data.get('student_id')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='student'
        )
        
        # Create student profile
        student = Student.objects.create(
            user=user,
            student_id=student_id
        )
        
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def student_login(request):
    """Student login endpoint"""
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.role != 'student':
            return Response(
                {'error': 'This account is not a student account'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get student profile
        student = Student.objects.get(user=user)
        serializer = StudentSerializer(student)
        
        return Response({
            'student': serializer.data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
        
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================
# STUDENT PROFILE MANAGEMENT
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_profile(request):
    """Get student profile"""
    try:
        student = request.user.student_profile
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student_profile(request):
    """Update student profile"""
    try:
        student = request.user.student_profile
        data = request.data
        
        # Update user fields
        user = request.user
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()
        
        # Update student fields
        student.phone = data.get('phone', student.phone)
        student.address = data.get('address', student.address)
        student.date_of_birth = data.get('date_of_birth', student.date_of_birth)
        student.save()
        
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================
# BOOK MANAGEMENT
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    """Get all books"""
    try:
        books = Book.objects.filter(is_active=True)
        
        # Search filter
        search = request.query_params.get('search')
        if search:
            books = books.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(isbn__icontains=search)
            )
        
        data = []
        for book in books:
            data.append({
                'id': str(book.id),
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'publisher': book.publisher,
                'publication_year': book.publication_year,
                'description': book.description,
                'quantity': book.quantity,
                'available_quantity': book.available_quantity,
                'location': book.location,
                'is_active': book.is_active,
            })
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_detail(request, book_id):
    """Get book details"""
    try:
        book = Book.objects.get(id=book_id, is_active=True)
        data = {
            'id': str(book.id),
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publisher': book.publisher,
            'publication_year': book.publication_year,
            'description': book.description,
            'quantity': book.quantity,
            'available_quantity': book.available_quantity,
            'location': book.location,
            'is_active': book.is_active,
        }
        return Response(data, status=status.HTTP_200_OK)
        
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ============================================
# EQUIPMENT MANAGEMENT
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment(request):
    """Get all equipment"""
    try:
        equipment = Equipment.objects.filter(is_active=True)
        
        # Filter by status
        status_filter = request.query_params.get('status')
        if status_filter:
            equipment = equipment.filter(status=status_filter)
        
        # Search filter
        search = request.query_params.get('search')
        if search:
            equipment = equipment.filter(
                Q(name__icontains=search) |
                Q(model__icontains=search) |
                Q(serial_number__icontains=search)
            )
        
        data = []
        for item in equipment:
            data.append({
                'id': str(item.id),
                'name': item.name,
                'model': item.model,
                'serial_number': item.serial_number,
                'description': item.description,
                'status': item.status,
                'location': item.location,
                'purchase_date': item.purchase_date,
                'warranty_expiry': item.warranty_expiry,
                'last_maintenance': item.last_maintenance,
                'notes': item.notes,
                'is_active': item.is_active,
            })
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment_detail(request, equipment_id):
    """Get equipment details"""
    try:
        item = Equipment.objects.get(id=equipment_id, is_active=True)
        data = {
            'id': str(item.id),
            'name': item.name,
            'model': item.model,
            'serial_number': item.serial_number,
            'description': item.description,
            'status': item.status,
            'location': item.location,
            'purchase_date': item.purchase_date,
            'warranty_expiry': item.warranty_expiry,
            'last_maintenance': item.last_maintenance,
            'notes': item.notes,
            'is_active': item.is_active,
        }
        return Response(data, status=status.HTTP_200_OK)
        
    except Equipment.DoesNotExist:
        return Response(
            {'error': 'Equipment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )