from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page, name='search_page'),
    path('dashboard-page/', views.dashboard_page, name='dashboard-page'),
    path('login/', views.student_login, name='student_login'),
    path('student-login/', views.student_login_page, name='student_login_page'),
    path('student-login-action/', views.student_login_action, name='student_login_action'),
    path('student-portal/', views.student_portal, name='student_portal'),
    path('student-logout/', views.student_logout_action, name='student_logout_action'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.student_logout, name='student_logout'),
    path('search/', views.LessonSearchView.as_view(), name='lesson-search'),
    path('filter-options/', views.FilterOptionsView.as_view(), name='filter-options'),
    path('quiz-list/', views.quiz_list, name='quiz_list'),
    path('take-quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
]