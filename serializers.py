from rest_framework import serializers
from .models import Lesson, Subject, Grade

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    grade_level = serializers.CharField(source='grade.level', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'topic', 'subject', 'subject_name', 
                 'grade', 'grade_level', 'content_type', 'description']