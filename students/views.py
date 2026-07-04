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