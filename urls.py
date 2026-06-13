from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.LessonSearchView.as_view(), name='lesson-search'),
    path('api/filter-options/', views.FilterOptionsView.as_view(), name='filter-options'),
]