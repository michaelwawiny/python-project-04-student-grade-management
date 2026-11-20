import unittest
import tempfile
import os

from student import Student
from grade_manager import GradeManager
from database import Database


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(
            "J25-001",
            "Michael",
            "Mathematics and Computer Science"
        )

    def test_student_registration(self):
        self.assertEqual(self.student.name, "Michael")

    def test_add_marks(self):
        self.student.add_mark("Python", 85)

        self.assertEqual(self.student.marks["Python"], 85)

    def test_invalid_marks(self):
        with self.assertRaises(ValueError):
            self.student.add_mark("Python", 120)

    def test_calculate_average(self):
        self.student.add_mark("Python", 80)
        self.student.add_mark("Mathematics", 90)

        self.assertEqual(self.student.calculate_average(), 85)

    def test_calculate_total(self):
        self.student.add_mark("Python", 80)
        self.student.add_mark("Mathematics", 90)

        self.assertEqual(self.student.calculate_total(), 170)

    def test_grade_assignment(self):
        self.student.add_mark("Python", 85)

        self.assertEqual(self.student.get_grade(), "A")


class TestGradeManager(unittest.TestCase):

    def setUp(self):
        self.manager = GradeManager()

    def test_add_student(self):
        student = self.manager.add_student(
            "J25-002",
            "John",
            "Computer Science"
        )

        self.assertEqual(student.name, "John")

    def test_duplicate_student(self):
        self.manager.add_student(
            "J25-002",
            "John",
            "Computer Science"
        )

        with self.assertRaises(ValueError):
            self.manager.add_student(
                "J25-002",
                "Peter",
                "Mathematics"
            )

    def test_search_student(self):
        self.manager.add_student(
            "J25-003",
            "Peter",
            "Mathematics"
        )

        student = self.manager.get_student("J25-003")

        self.assertEqual(student.name, "Peter")

    def test_delete_student(self):
        self.manager.add_student(
            "J25-004",
            "Mary",
            "Computer Science"
        )

        self.manager.delete_student("J25-004")

        self.assertIsNone(self.manager.get_student("J25-004"))

    def test_top_student(self):
        self.manager.add_student("J25-005", "John", "CS")
        self.manager.add_student("J25-006", "Mary", "CS")

        self.manager.update_student_mark("J25-005", "Python", 60)
        self.manager.update_student_mark("J25-006", "Python", 90)

        top = self.manager.get_top_student()

        self.assertEqual(top.name, "Mary")


class TestDatabase(unittest.TestCase):

    def test_save_and_load_students(self):

        with tempfile.TemporaryDirectory() as directory:

            filename = os.path.join(directory, "students.json")

            database = Database(filename)

            student = Student("J25-007", "David", "Computer Science")
            student.add_mark("Python", 95)

            database.save_students([student])

            loaded_students = database.load_students()

            self.assertEqual(len(loaded_students), 1)
            self.assertEqual(loaded_students[0].name, "David")
            self.assertEqual(loaded_students[0].marks["Python"], 95)


if __name__ == "__main__":
    unittest.main()