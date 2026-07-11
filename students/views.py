from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
# ============================================
# STUDENT REGISTRATION & LOGIN (from mobile_views)
# ============================================
@api_view(['POST'])
@permission_classes([AllowAny])
def student_register(request):
    """Student registration endpoint"""
    # This is already in your mobile_views.py
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def student_login(request):
    """Student login endpoint"""
    # This is already in your mobile_views.py
    pass

# ============================================
# DASHBOARD API
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request):
    """Get dashboard data for the logged-in student"""
    # Add the function we wrote earlier
    pass
# ============================================
# DASHBOARD API VIEW
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request):
    """Get dashboard data for the logged-in student"""
    try:
        # Get the student profile
        student = request.user.student_profile
        
        # Sample data - in production, this comes from database
        data = {
            'student_name': student.user.get_full_name() or 'Student',
            'total_courses': 4,
            'avg_grade': 70,
            'completed_lessons': 30,
            'overall_progress': 53,
            'courses': [
                {'name': 'Mathematics', 'progress': 75, 'grade': 'A', 'score': 92},
                {'name': 'English', 'progress': 60, 'grade': 'B', 'score': 78},
                {'name': 'Chemistry', 'progress': 45, 'grade': 'C', 'score': 65},
                {'name': 'Physics', 'progress': 30, 'grade': 'D', 'score': 45}
            ],
            'grades': [
                {'subject': 'Mathematics', 'score': 92, 'grade': 'A'},
                {'subject': 'English', 'score': 78, 'grade': 'B'},
                {'subject': 'Chemistry', 'score': 65, 'grade': 'C'},
                {'subject': 'Physics', 'score': 45, 'grade': 'D'}
            ],
            'activity': [
                {'action': 'Started new course: Mathematics', 'date': '2 days ago'},
                {'action': 'Completed Lesson 5', 'date': '3 days ago'},
                {'action': 'Scored 92% on Math Quiz', 'date': '5 days ago'}
            ]
        }
        
        return Response({
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
# ============================================
# DASHBOARD API VIEW
# ============================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request):
    """Get dashboard data for the logged-in student"""
    try:
        # Get the student profile
        student = request.user.student_profile
        
        # Sample data - in production, this comes from database
        data = {
            'student_name': student.user.get_full_name() or 'Student',
            'total_courses': 4,
            'avg_grade': 70,
            'completed_lessons': 30,
            'overall_progress': 53,
            'courses': [
                {'name': 'Mathematics', 'progress': 75, 'grade': 'A', 'score': 92},
                {'name': 'English', 'progress': 60, 'grade': 'B', 'score': 78},
                {'name': 'Chemistry', 'progress': 45, 'grade': 'C', 'score': 65},
                {'name': 'Physics', 'progress': 30, 'grade': 'D', 'score': 45}
            ],
            'grades': [
                {'subject': 'Mathematics', 'score': 92, 'grade': 'A'},
                {'subject': 'English', 'score': 78, 'grade': 'B'},
                {'subject': 'Chemistry', 'score': 65, 'grade': 'C'},
                {'subject': 'Physics', 'score': 45, 'grade': 'D'}
            ],
            'activity': [
                {'action': 'Started new course: Mathematics', 'date': '2 days ago'},
                {'action': 'Completed Lesson 5', 'date': '3 days ago'},
                {'action': 'Scored 92% on Math Quiz', 'date': '5 days ago'}
            ]
        }
        
        return Response({
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )