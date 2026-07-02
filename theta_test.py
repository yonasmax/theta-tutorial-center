# --- THETA TUTORIAL CENTER: STUDENT DATABASE CHECKER ---

print("--- Welcome to Theta Tutorial Center ---")

# This is our mock database of registered students and their grades
# Format: "Student Name": "Grade"
registered_students = {
    "Yonas Molla": "11",
    "Abebe Kebede": "9",
    "Chala Tolosa": "12",
    "Aster Assefa": "10"
}

# 1. Ask for the student's name
name_input = raw_input("Enter your full name to log in: ")

# 2. Check if the student exists in our "database"
if name_input in registered_students:
    # If they exist, find their grade
    student_grade = registered_students[name_input]
    print("\nLogin Successful! Welcome back, " + name_input + ".")
    print("You are registered in Grade " + student_grade + ".")
    
    # Show their specific subjects
    if student_grade == "11":
        print("\nYour Grade 11 Subjects:")
        print("- Mathematics, Physics, Chemistry, Biology")
    elif student_grade == "9":
        print("\nYour Grade 9 Subjects:")
        print("- Mathematics, Physics, Chemistry")
        
else:
    # If the name is not in our database
    print("\nACCESS DENIED!")
    print("Error: '" + name_input + "' is not registered in Theta Tutorial Center.")
    print("Please contact the Admin to register.")
        python manage.py createsuperuser

    python manage.py createsuperuser

