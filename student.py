class Student:
    def __init__(self, admission_number, name, course):
        self.admission_number = admission_number
        self.name = name
        self.course = course
        self.marks = {}

    def add_mark(self, subject, mark):
        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        self.marks[subject] = mark

    def calculate_average(self):
        if not self.marks:
            return 0

        return sum(self.marks.values()) / len(self.marks)

    def calculate_total(self):
        return sum(self.marks.values())

    def get_grade(self):
        average = self.calculate_average()

        if average >= 70:
            return "A"
        elif average >= 60:
            return "B"
        elif average >= 50:
            return "C"
        elif average >= 40:
            return "D"
        else:
            return "E"

    def to_dict(self):
        return {
            "admission_number": self.admission_number,
            "name": self.name,
            "course": self.course,
            "marks": self.marks,
            "average": self.calculate_average(),
            "grade": self.get_grade()
        }