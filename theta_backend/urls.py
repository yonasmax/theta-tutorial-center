from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
import os

# Simple view to serve HTML files
def serve_html(request, filename='index.html'):
    try:
        # Try frontend folder first
        filepath = os.path.join('frontend', filename)
        if not os.path.exists(filepath):
            # Try static folder
            filepath = os.path.join('static', filename)
        if not os.path.exists(filepath):
            # Try with .html extension
            if not filename.endswith('.html'):
                filepath = os.path.join('frontend', filename + '.html')
                if not os.path.exists(filepath):
                    filepath = os.path.join('static', filename + '.html')
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return HttpResponse(content, content_type='text/html')
    except Exception as e:
        return HttpResponse(f"<h1>File Not Found</h1><p>Error: {str(e)}</p>", status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', serve_html, name='home'),
    path('frontend/<path:filename>', serve_html, name='frontend'),
    path('static/<path:filename>', serve_html, name='static'),
    path('dashboard/', serve_html, name='dashboard'),  # 👈 SHORTCUT URL
    path('api/', include('students.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/library/', include('library.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)