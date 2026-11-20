from student import Student


class GradeManager:

    def __init__(self):
        self.students = {}

    # CREATE: Register a student
    def add_student(self, admission_number, name, course):

        if admission_number in self.students:
            raise ValueError("Student already exists.")

        student = Student(admission_number, name, course)

        self.students[admission_number] = student

        return student

    # READ: Get all students
    def get_all_students(self):
        return list(self.students.values())

    # READ: Search for a student
    def get_student(self, admission_number):
        return self.students.get(admission_number)

    # UPDATE: Add or update student marks
    def update_student_mark(self, admission_number, subject, mark):

        student = self.get_student(admission_number)

        if student is None:
            raise ValueError("Student not found.")

        student.add_mark(subject, mark)

    # DELETE: Remove a student
    def delete_student(self, admission_number):

        if admission_number not in self.students:
            raise ValueError("Student not found.")

        del self.students[admission_number]

    # GET: Find the top-performing student
    def get_top_student(self):

        students_with_marks = [
            student for student in self.students.values()
            if student.marks
        ]

        if not students_with_marks:
            return None

        return max(
            students_with_marks,
            key=lambda student: student.calculate_average()
        )

    # REPORT: Display student performance
    def generate_report(self):

        report = []

        for student in self.students.values():

            report.append({
                "admission_number": student.admission_number,
                "name": student.name,
                "course": student.course,
                "total": student.calculate_total(),
                "average": round(student.calculate_average(), 2),
                "grade": student.get_grade()
            })

        return report
    