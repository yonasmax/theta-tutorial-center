import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Theta_Tutorial_Center_backend.settings')
django.setup()

from your_app.models import Book  # 🔴 CHANGE 'your_app' to your actual app name

# List all PDFs in the handouts folder
books = [
    {
        'title': 'Chemistry Grade 9',
        'author': 'Unknown',
        'pages': 100,
        'grade': 9,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_grade9.pdf'
    },
    {
        'title': 'Chemistry Grade 9 (Alternative)',
        'author': 'Unknown',
        'pages': 95,
        'grade': 9,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_grade9_alternative.pdf'
    },
    {
        'title': 'Compost & Organic Fertilizer Production',
        'author': 'FAO',
        'pages': 80,
        'grade': 10,
        'subject': 'Agriculture',
        'file_path': 'handouts/compost_production.pdf'
    },
    {
        'title': 'FAO Handbook for Saline Soil Management',
        'author': 'FAO',
        'pages': 120,
        'grade': 10,
        'subject': 'Agriculture',
        'file_path': 'handouts/saline_soil_handbook.pdf'
    },
    {
        'title': 'Green Field HRM',
        'author': 'Unknown',
        'pages': 150,
        'grade': 12,
        'subject': 'Business',
        'file_path': 'handouts/green_field_hrm.pdf'
    },
    {
        'title': 'My Blue Print',
        'author': 'Unknown',
        'pages': 60,
        'grade': 11,
        'subject': 'Career',
        'file_path': 'handouts/my_blueprint.pdf'
    },
    {
        'title': 'አማርኛ መዝገበ ቃላት (Amharic Dictionary)',
        'author': 'Unknown',
        'pages': 200,
        'grade': 10,
        'subject': 'Amharic',
        'file_path': 'handouts/amharic_dictionary.pdf'
    },
    {
        'title': 'Assignment 17',
        'author': 'Teacher',
        'pages': 10,
        'grade': 10,
        'subject': 'General',
        'file_path': 'handouts/assignment_17.pdf'
    }
]

for book in books:
    try:
        Book.objects.create(
            title=book['title'],
            author=book['author'],
            pages=book['pages'],
            grade_level=book['grade'],
            subject=book['subject'],
            file_path=book['file_path'],
            uploaded_by='Almaz Desta'
        )
        print(f"✅ Added: {book['title']}")
    except Exception as e:
        print(f"❌ Error adding {book['title']}: {e}")

print("\n✅ All books added successfully!")