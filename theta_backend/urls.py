from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/lab-library/', include('lab_library.urls')),
]