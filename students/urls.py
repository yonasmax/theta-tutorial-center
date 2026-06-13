from django.urls import path
from . import views

urlpatterns = [
    # Test URL
    path('test/', views.test_progress, name='test-progress'),
    
    # Student URLs
    path('students/', views.StudentListView.as_view(), name='student-list'),
    
    # Progress Tracking URLs
    path('progress/', views.StudentProgressListView.as_view(), name='progress-list'),
    path('update-progress/', views.UpdateProgressView.as_view(), name='update-progress'),
    path('dashboard/<int:student_id>/', views.StudentDashboardView.as_view(), name='student-dashboard'),
    path('submit-quiz/', views.SubmitQuizScoreView.as_view(), name='submit-quiz'),
    
    # Search URLs
    path('search/', views.LessonSearchView.as_view(), name='lesson-search'),
    path('filter-options/', views.FilterOptionsView.as_view(), name='filter-options'),
    
    # Certificate URLs
    path('certificates/<int:student_id>/', views.StudentCertificatesView.as_view(), name='student-certificates'),
    path('generate-certificate/', views.GenerateCertificateView.as_view(), name='generate-certificate'),
    path('download-certificate/<int:certificate_id>/', views.DownloadCertificateView.as_view(), name='download-certificate'),
    path('send-certificate-email/', views.SendCertificateEmailView.as_view(), name='send-certificate-email'),
    path('send-progress-report/', views.SendProgressReportView.as_view(), name='send-progress-report'),
    
    # Mobile API URLs
    path('mobile/login/', views.MobileLoginView.as_view(), name='mobile-login'),
    path('mobile/dashboard/<int:student_id>/', views.MobileDashboardView.as_view(), name='mobile-dashboard'),
    path('mobile/lesson/<int:student_id>/<int:lesson_id>/', views.MobileLessonDetailView.as_view(), name='mobile-lesson'),
    path('mobile/update-progress/', views.MobileUpdateProgressView.as_view(), name='mobile-update-progress'),
    path('mobile/library/', views.MobileLibraryView.as_view(), name='mobile-library'),
    path('mobile/equipment/', views.MobileEquipmentView.as_view(), name='mobile-equipment'),
    path('mobile/notifications/<int:student_id>/', views.MobileNotificationsView.as_view(), name='mobile-notifications'),
]