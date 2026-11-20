from grade_manager import GradeManager
from database import Database


# INITIALIZE APPLICATION
manager = GradeManager()
database = Database()

# LOAD EXISTING STUDENTS
for student in database.load_students():
    manager.add_student(
        student.admission_number,
        student.name,
        student.course
    )

    for subject, mark in student.marks.items():
        manager.update_student_mark(
            student.admission_number,
            subject,
            mark
        )


# REGISTER STUDENT
def register_student():

    print("\n--- REGISTER STUDENT ---")

    admission = input("Admission Number: ").strip()
    name = input("Student Name: ").strip()
    course = input("Course: ").strip()

    if not admission or not name or not course:
        print("All fields are required.")
        return

    try:
        manager.add_student(admission, name, course)
        database.save_students(manager.get_all_students())

        print("Student registered successfully!")

    except ValueError as error:
        print(error)


# ADD STUDENT MARKS
def add_marks():

    print("\n--- ADD STUDENT MARKS ---")

    admission = input("Admission Number: ").strip()
    subject = input("Subject: ").strip()

    if not subject:
        print("Subject is required.")
        return

    try:
        mark = float(input("Enter Marks (0-100): "))

        manager.update_student_mark(admission, subject, mark)

        database.save_students(manager.get_all_students())

        print("Marks added successfully!")

    except ValueError as error:
        print(f"Error: {error}")


# VIEW ALL STUDENTS
def view_students():

    print("\n--- STUDENT RECORDS ---")

    students = manager.get_all_students()

    if not students:
        print("No students registered.")
        return

    for student in students:

        print("\nAdmission:", student.admission_number)
        print("Name:", student.name)
        print("Course:", student.course)
        print("Average:", round(student.calculate_average(), 2))
        print("Grade:", student.get_grade())


# SEARCH STUDENT
def search_student():

    print("\n--- SEARCH STUDENT ---")

    admission = input("Enter Admission Number: ").strip()

    student = manager.get_student(admission)

    if student:
        print("\nName:", student.name)
        print("Course:", student.course)
        print("Marks:", student.marks)
        print("Average:", round(student.calculate_average(), 2))
        print("Grade:", student.get_grade())

    else:
        print("Student not found.")


# DELETE STUDENT
def delete_student():

    print("\n--- DELETE STUDENT ---")

    admission = input("Enter Admission Number: ").strip()

    try:
        manager.delete_student(admission)
        database.save_students(manager.get_all_students())

        print("Student deleted successfully!")

    except ValueError as error:
        print(error)


# TOP STUDENT
def top_student():

    print("\n--- TOP PERFORMING STUDENT ---")

    student = manager.get_top_student()

    if student:
        print("Name:", student.name)
        print("Average:", round(student.calculate_average(), 2))
        print("Grade:", student.get_grade())

    else:
        print("No student marks available.")


# PERFORMANCE REPORT
def performance_report():

    print("\n--- PERFORMANCE REPORT ---")

    report = manager.generate_report()

    if not report:
        print("No records available.")
        return

    for record in report:

        print("\nStudent:", record["name"])
        print("Admission:", record["admission_number"])
        print("Total:", record["total"])
        print("Average:", record["average"])
        print("Grade:", record["grade"])


# MAIN MENU
def main():

    while True:

        print("\n================================")
        print(" STUDENT GRADE MANAGEMENT SYSTEM")
        print("================================")

        print("1. Register Student")
        print("2. Add Student Marks")
        print("3. View All Students")
        print("4. Search Student")
        print("5. Delete Student")
        print("6. Top Performing Student")
        print("7. Performance Report")
        print("8. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            register_student()

        elif choice == "2":
            add_marks()

        elif choice == "3":
            view_students()

        elif choice == "4":
            search_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            top_student()

        elif choice == "7":
            performance_report()

        elif choice == "8":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()