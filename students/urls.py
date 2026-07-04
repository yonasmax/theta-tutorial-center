from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # TEST URL
    # ==========================================
    path('test/', views.test_progress, name='test-progress'),
    
    # ==========================================
    # STUDENT CRUD URLs
    # ==========================================
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<uuid:id>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<uuid:id>/update/', views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<uuid:id>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
    path('students/bulk-upload/', views.StudentBulkUploadView.as_view(), name='student-bulk-upload'),
    path('students/stats/', views.StudentStatsView.as_view(), name='student-stats'),
    path('students/search/', views.search_students, name='student-search'),
    
    # ==========================================
    # PROGRESS TRACKING URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('progress/', views.StudentProgressListView.as_view(), name='progress-list'),
    # path('update-progress/', views.UpdateProgressView.as_view(), name='update-progress'),
    # path('dashboard/<int:student_id>/', views.StudentDashboardView.as_view(), name='student-dashboard'),
    # path('submit-quiz/', views.SubmitQuizScoreView.as_view(), name='submit-quiz'),
    
    # ==========================================
    # SEARCH URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('search/', views.LessonSearchView.as_view(), name='lesson-search'),
    # path('filter-options/', views.FilterOptionsView.as_view(), name='filter-options'),
    
    # ==========================================
    # CERTIFICATE URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('certificates/<int:student_id>/', views.StudentCertificatesView.as_view(), name='student-certificates'),
    # path('generate-certificate/', views.GenerateCertificateView.as_view(), name='generate-certificate'),
    # path('download-certificate/<int:certificate_id>/', views.DownloadCertificateView.as_view(), name='download-certificate'),
    # path('send-certificate-email/', views.SendCertificateEmailView.as_view(), name='send-certificate-email'),
    # path('send-progress-report/', views.SendProgressReportView.as_view(), name='send-progress-report'),
    
    # ==========================================
    # MOBILE API URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('mobile/login/', views.MobileLoginView.as_view(), name='mobile-login'),
    # path('mobile/dashboard/<int:student_id>/', views.MobileDashboardView.as_view(), name='mobile-dashboard'),
    # path('mobile/lesson/<int:student_id>/<int:lesson_id>/', views.MobileLessonDetailView.as_view(), name='mobile-lesson'),
    # path('mobile/update-progress/', views.MobileUpdateProgressView.as_view(), name='mobile-update-progress'),
    # path('mobile/library/', views.MobileLibraryView.as_view(), name='mobile-library'),
    # path('mobile/equipment/', views.MobileEquipmentView.as_view(), name='mobile-equipment'),
    # path('mobile/notifications/<int:student_id>/', views.MobileNotificationsView.as_view(), name='mobile-notifications'),
    
    # ==========================================
    # QUIZ SYSTEM URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    # path('quiz/lesson/<int:lesson_id>/', views.LessonQuizView.as_view(), name='lesson-quiz'),
    # path('quiz/start/', views.StartQuizView.as_view(), name='start-quiz'),
    # path('quiz/submit/', views.SubmitQuizView.as_view(), name='submit-quiz'),
    # path('quiz/result/<int:attempt_id>/', views.QuizResultView.as_view(), name='quiz-result'),
    
    # ==========================================
    # NOTES URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('notes/', views.NoteListView.as_view(), name='note-list'),
    # path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    # path('notes/create/', views.NoteCreateView.as_view(), name='note-create'),
    # path('notes/update/<int:pk>/', views.NoteUpdateView.as_view(), name='note-update'),
    # path('notes/delete/<int:pk>/', views.NoteDeleteView.as_view(), name='note-delete'),
    # path('notes/stats/', views.NoteStatsView.as_view(), name='note-stats'),
    
    # ==========================================
    # GRADE 10 URLs (COMMENTED OUT - Add views later)
    # ==========================================
    # path('grade10/dashboard/<int:student_id>/', views.Grade10DashboardView.as_view(), name='grade10-dashboard'),
    # path('grade10/subjects/', views.Grade10SubjectsView.as_view(), name='grade10-subjects'),
    # path('grade10/lessons/', views.Grade10LessonsView.as_view(), name='grade10-lessons'),
    # path('grade10/notes/', views.Grade10NotesView.as_view(), name='grade10-notes'),
    # path('grade10/quizzes/', views.Grade10QuizzesView.as_view(), name='grade10-quizzes'),
]