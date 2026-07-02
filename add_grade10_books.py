import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Theta_Tutorial_Center_backend.settings')
django.setup()

from your_app.models import Book  # 🔴 CHANGE 'your_app'

books = [
    {
        'title': 'Types of Chemical Reactions',
        'author': 'Almaz Desta',
        'pages': 15,
        'grade': 10,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_types_of_reactions.pdf'
    },
    {
        'title': 'Oxidation and Reduction (Redox Reactions)',
        'author': 'Almaz Desta',
        'pages': 12,
        'grade': 10,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_redox_reactions.pdf'
    },
    {
        'title': 'Reactivity Series of Metals',
        'author': 'Almaz Desta',
        'pages': 10,
        'grade': 10,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_reactivity_series.pdf'
    },
    {
        'title': 'Introduction to Chemical Equations',
        'author': 'Almaz Desta',
        'pages': 18,
        'grade': 10,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_chemical_equations.pdf'
    },
    {
        'title': 'Acids, Bases, and Salts',
        'author': 'Almaz Desta',
        'pages': 20,
        'grade': 10,
        'subject': 'Chemistry',
        'file_path': 'handouts/chemistry_acids_bases_salts.pdf'
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
        print(f"❌ Error: {e}")