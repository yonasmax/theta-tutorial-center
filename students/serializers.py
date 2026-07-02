from rest_framework import serializers
from .models import Lesson, Subject, Grade, Student, StudentProgress, QuizScore, Certificate, Quiz, Question, Choice, QuizAttempt, StudentAnswer, Note

class LessonSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    grade_level = serializers.CharField(source='grade.level', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'topic', 'subject', 'subject_name', 
                 'grade', 'grade_level', 'content_type', 'description', 'video_url']

class StudentSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'grade', 'payment_status', 'email', 'phone', 
                  'registered_date', 'profile_picture', 'profile_picture_url']
    
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'grade', 'description']

class StudentProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = ['id', 'student', 'student_name', 'lesson', 'lesson_title', 
                  'status', 'progress_percentage', 'started_at', 'last_accessed', 'completed_at']

class QuizScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = QuizScore
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True, allow_null=True)
    
    class Meta:
        model = Certificate
        fields = ['id', 'student', 'student_name', 'certificate_type', 'lesson', 'lesson_title', 
                  'certificate_number', 'issued_date', 'is_downloaded']

# ========== QUIZ SERIALIZERS ==========

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'lesson', 'lesson_title', 'title', 'description', 'time_limit_minutes', 'passing_score', 'questions']

class QuizAttemptSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = '__all__'

# ========== NOTE SERIALIZER ==========

class NoteSerializer(serializers.ModelSerializer):
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    pdf_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'subject', 'subject_display', 'grade', 'grade_display', 
                  'topic', 'content', 'summary', 'pdf_url', 'image_url', 
                  'created_at', 'updated_at', 'view_count', 'download_count']
    
    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return obj.pdf_file.url
        return None
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None