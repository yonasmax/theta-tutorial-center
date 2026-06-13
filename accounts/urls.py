from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page, name='search_page'),
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.student_logout, name='student_logout'),
    path('search/', views.LessonSearchView.as_view(), name='lesson-search'),
    path('filter-options/', views.FilterOptionsView.as_view(), name='filter-options'),
]