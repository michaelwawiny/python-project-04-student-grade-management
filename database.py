import json
import os

from student import Student


class Database:

    def __init__(self, filename="data/students.json"):

        self.filename = filename

        directory = os.path.dirname(self.filename)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filename):
            self.save_students([])


    def save_students(self, students):

        data = {
            "students": [
                {
                    "admission_number": student.admission_number,
                    "name": student.name,
                    "course": student.course,
                    "marks": student.marks
                }
                for student in students
            ]
        }

        with open(
            self.filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(data, file, indent=4)


    def load_students(self):

        with open(
            self.filename,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        students = []

        for record in data["students"]:

            student = Student(
                record["admission_number"],
                record["name"],
                record["course"]
            )

            for subject, mark in record["marks"].items():

                student.add_mark(subject, mark)

            students.append(student)

        return students