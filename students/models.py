from django.db import models

class Student(models.Model):
    GRADE_CHOICES = [
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    
    PAYMENT_CHOICES = [
        ('Paid', 'Paid ✓'),
        ('Not Paid', 'Not Paid ✗'),
    ]
    
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Not Paid')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.grade}"

class Subject(models.Model):
    GRADE_CHOICES = [
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} (Grade {self.grade})"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.student.name} - ${self.amount} - {'Paid' if self.is_paid else 'Not Paid'}"

class Grade(models.Model):
    level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.level

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='lessons')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name='lessons')
    content_type = models.CharField(
        max_length=20,
        choices=[('video', 'Video'), ('quiz', 'Quiz'), ('article', 'Article')]
    )
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
# ========== STUDENT PROGRESS TRACKING MODELS ==========

class StudentProgress(models.Model):
    """Tracks which lessons a student has completed"""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.IntegerField(default=0)  # 0-100
    started_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'lesson']  # One record per student per lesson
        ordering = ['-last_accessed']
    
    def __str__(self):
        return f"{self.student.name} - {self.lesson.title} ({self.status})"

class QuizScore(models.Model):
    """Tracks student quiz scores"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_scores')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz_scores')
    score = models.IntegerField()  # Score out of 100
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.lesson.title}: {self.score}%"

class StudentActivity(models.Model):
    """Tracks general student activity (login, search, etc.)"""
    
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('search', 'Search'),
        ('view_lesson', 'Viewed Lesson'),
        ('take_quiz', 'Took Quiz'),
        ('borrow_book', 'Borrowed Book'),
        ('make_payment', 'Made Payment'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.activity_type} at {self.timestamp}"
# ========== STUDENT PROGRESS TRACKING MODELS ==========

class StudentProgress(models.Model):
    """Tracks which lessons a student has completed"""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='student_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'lesson']
        ordering = ['-last_accessed']
    
    def __str__(self):
        return f"{self.student.name} - {self.lesson.title} ({self.status})"

class QuizScore(models.Model):
    """Tracks student quiz scores"""
    
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='quiz_scores')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='quiz_scores')
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.lesson.title}: {self.score}%"

class StudentActivity(models.Model):
    """Tracks general student activity"""
    
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('search', 'Search'),
        ('view_lesson', 'Viewed Lesson'),
        ('take_quiz', 'Took Quiz'),
        ('borrow_book', 'Borrowed Book'),
        ('make_payment', 'Made Payment'),
    ]
    
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.activity_type}"
# ========== CERTIFICATE MODEL ==========

class Certificate(models.Model):
    """Tracks certificates issued to students"""
    
    CERTIFICATE_TYPES = [
        ('course_completion', 'Course Completion'),
        ('quiz_achievement', 'Quiz Achievement'),
        ('attendance', 'Attendance Certificate'),
        ('excellence', 'Excellence Award'),
    ]
    
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='certificates')
    certificate_type = models.CharField(max_length=30, choices=CERTIFICATE_TYPES)
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_downloaded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.name} - {self.get_certificate_type_display()} - {self.certificate_number}"
# ========== QUIZ SYSTEM MODELS ==========

class Quiz(models.Model):
    """Represents a quiz for a lesson"""
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit_minutes = models.IntegerField(default=30)
    passing_score = models.IntegerField(default=70)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Quiz: {self.title}"

class Question(models.Model):
    """Represents a question in a quiz"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"

class Choice(models.Model):
    """Represents a choice for multiple choice questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text

class QuizAttempt(models.Model):
    """Tracks a student's attempt at a quiz"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.quiz.title} - {self.percentage}%"

class StudentAnswer(models.Model):
    """Stores individual answers for each question"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Answer for Q{self.question.id}: {'Correct' if self.is_correct else 'Incorrect'}"