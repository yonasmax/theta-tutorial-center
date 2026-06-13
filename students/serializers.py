from rest_framework import serializers
from .models import Lesson, Subject, Grade, Student, StudentProgress, QuizScore, Certificate, Quiz, Question, Choice, QuizAttempt, StudentAnswer

class LessonSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    grade_level = serializers.CharField(source='grade.level', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'topic', 'subject', 'subject_name', 
                 'grade', 'grade_level', 'content_type', 'description']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'grade', 'payment_status']

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