import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theta_backend.settings')
django.setup()

from students.models import Subject, Grade, Lesson

# Create grades
g9, _ = Grade.objects.get_or_create(level="Grade 9")
g10, _ = Grade.objects.get_or_create(level="Grade 10")
g11, _ = Grade.objects.get_or_create(level="Grade 11")
g12, _ = Grade.objects.get_or_create(level="Grade 12")
print("✓ Grades created")

# Create subjects
math, _ = Subject.objects.get_or_create(name="Mathematics", grade="10")
science, _ = Subject.objects.get_or_create(name="Science", grade="10")
english, _ = Subject.objects.get_or_create(name="English", grade="10")
history, _ = Subject.objects.get_or_create(name="History", grade="10")
geez, _ = Subject.objects.get_or_create(name="Geez", grade="10")
print("✓ Subjects created")

# Create lessons
Lesson.objects.get_or_create(
    title="Algebra Basics",
    defaults={
        "topic": "Algebra",
        "subject": math,
        "grade": g10,
        "content_type": "video",
        "description": "Learn the fundamentals of algebra"
    }
)

Lesson.objects.get_or_create(
    title="Quadratic Equations",
    defaults={
        "topic": "Algebra",
        "subject": math,
        "grade": g10,
        "content_type": "quiz",
        "description": "Test your knowledge of quadratic equations"
    }
)

Lesson.objects.get_or_create(
    title="Cell Structure",
    defaults={
        "topic": "Biology",
        "subject": science,
        "grade": g10,
        "content_type": "video",
        "description": "Introduction to cell biology"
    }
)

Lesson.objects.get_or_create(
    title="Grammar Essentials",
    defaults={
        "topic": "Grammar",
        "subject": english,
        "grade": g10,
        "content_type": "article",
        "description": "English grammar basics"
    }
)

Lesson.objects.get_or_create(
    title="Ancient Civilizations",
    defaults={
        "topic": "World History",
        "subject": history,
        "grade": g10,
        "content_type": "video",
        "description": "Learn about ancient civilizations"
    }
)

Lesson.objects.get_or_create(
    title="Geez Alphabet",
    defaults={
        "topic": "Geez Script",
        "subject": geez,
        "grade": g9,
        "content_type": "video",
        "description": "Introduction to Geez characters"
    }
)

print(f"✓ Success! Total lessons: {Lesson.objects.count()}")