from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import os

# Simple view to serve HTML files
def serve_html(request, filename='index.html'):
    try:
        # Try frontend folder first
        filepath = os.path.join('frontend', filename)
        if not os.path.exists(filepath):
            # Try static folder
            filepath = os.path.join('static', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return HttpResponse(content, content_type='text/html')
    except Exception as e:
        return HttpResponse(f"<h1>File Not Found</h1><p>Error: {str(e)}</p>", status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', serve_html, name='home'),
    path('frontend/<path:filename>', serve_html, name='frontend'),
    path('api/', include('students.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/library/', include('library.urls')),
]