from rest_framework import serializers
from .models import Student
from accounts.models import User


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'email', 'first_name', 'last_name',
            'phone', 'address', 'date_of_birth', 'enrollment_date',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'enrollment_date']


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for Student profile"""
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'email', 'first_name', 'last_name',
            'phone', 'address', 'date_of_birth', 'enrollment_date',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'student_id', 'created_at', 'updated_at', 'enrollment_date']
    
    def update(self, instance, validated_data):
        """Update student and user fields"""
        user_data = validated_data.pop('user', {})
        
        # Update user fields
        user = instance.user
        if 'first_name' in user_data:
            user.first_name = user_data.get('first_name', user.first_name)
        if 'last_name' in user_data:
            user.last_name = user_data.get('last_name', user.last_name)
        if 'email' in user_data:
            user.email = user_data.get('email', user.email)
        user.save()
        
        # Update student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class StudentRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for student registration"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'email', 'password', 'first_name', 
            'last_name', 'phone', 'address', 'date_of_birth'
        ]
    
    def create(self, validated_data):
        """Create user and student profile"""
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='student'
        )
        
        # Create student
        student = Student.objects.create(user=user, **validated_data)
        return student


class StudentLoginSerializer(serializers.Serializer):
    """Serializer for student login"""
    email = serializers.EmailField()
    password = serializers.CharField()


# ============================================
# LESSON SERIALIZERS
# ============================================

class LessonSerializer(serializers.Serializer):
    """Serializer for lessons"""
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    course_id = serializers.UUIDField()
    instructor_id = serializers.UUIDField()
    date = serializers.DateTimeField()
    duration = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class LessonCreateSerializer(serializers.Serializer):
    """Serializer for creating lessons"""
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    course_id = serializers.UUIDField()
    instructor_id = serializers.UUIDField()
    date = serializers.DateTimeField()
    duration = serializers.IntegerField()


class LessonUpdateSerializer(serializers.Serializer):
    """Serializer for updating lessons"""
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    course_id = serializers.UUIDField(required=False)
    instructor_id = serializers.UUIDField(required=False)
    date = serializers.DateTimeField(required=False)
    duration = serializers.IntegerField(required=False)


# ============================================
# ATTENDANCE SERIALIZERS
# ============================================

class AttendanceSerializer(serializers.Serializer):
    """Serializer for attendance"""
    id = serializers.UUIDField()
    student_id = serializers.UUIDField()
    lesson_id = serializers.UUIDField()
    status = serializers.CharField()
    check_in_time = serializers.DateTimeField()
    notes = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AttendanceCreateSerializer(serializers.Serializer):
    """Serializer for creating attendance"""
    student_id = serializers.UUIDField()
    lesson_id = serializers.UUIDField()
    status = serializers.CharField()
    check_in_time = serializers.DateTimeField()
    notes = serializers.CharField(required=False)


class AttendanceUpdateSerializer(serializers.Serializer):
    """Serializer for updating attendance"""
    status = serializers.CharField(required=False)
    check_in_time = serializers.DateTimeField(required=False)
    notes = serializers.CharField(required=False)


# ============================================
# GRADE SERIALIZERS
# ============================================

class GradeSerializer(serializers.Serializer):
    """Serializer for grades"""
    id = serializers.UUIDField()
    student_id = serializers.UUIDField()
    course_id = serializers.UUIDField()
    assignment_name = serializers.CharField()
    score = serializers.FloatField()
    max_score = serializers.FloatField()
    grade = serializers.CharField()
    feedback = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GradeCreateSerializer(serializers.Serializer):
    """Serializer for creating grades"""
    student_id = serializers.UUIDField()
    course_id = serializers.UUIDField()
    assignment_name = serializers.CharField()
    score = serializers.FloatField()
    max_score = serializers.FloatField()
    grade = serializers.CharField()
    feedback = serializers.CharField(required=False)


class GradeUpdateSerializer(serializers.Serializer):
    """Serializer for updating grades"""
    score = serializers.FloatField(required=False)
    max_score = serializers.FloatField(required=False)
    grade = serializers.CharField(required=False)
    feedback = serializers.CharField(required=False)


# ============================================
# ENROLLMENT SERIALIZERS
# ============================================

class EnrollmentSerializer(serializers.Serializer):
    """Serializer for enrollments"""
    id = serializers.UUIDField()
    student_id = serializers.UUIDField()
    course_id = serializers.UUIDField()
    enrollment_date = serializers.DateTimeField()
    status = serializers.CharField()
    completion_date = serializers.DateTimeField(required=False)
    progress = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class EnrollmentCreateSerializer(serializers.Serializer):
    """Serializer for creating enrollments"""
    student_id = serializers.UUIDField()
    course_id = serializers.UUIDField()
    status = serializers.CharField(required=False)
    progress = serializers.FloatField(required=False)