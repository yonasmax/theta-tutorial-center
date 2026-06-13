from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lesson, Subject, Grade
from .serializers import LessonSerializer

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
# ========== ADD THESE SEARCH VIEWS AT THE BOTTOM ==========
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lesson, Subject, Grade
from .serializers import LessonSerializer

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