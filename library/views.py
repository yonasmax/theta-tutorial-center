from django.http import HttpResponse

def index(request):
    return HttpResponse("""
        <h1>📚 Library API</h1>
        <p>Welcome to Theta Tutorial Center Library</p>
        <ul>
            <li><a href="/admin/">Admin Panel</a></li>
        </ul>
    """)