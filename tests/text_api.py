import unittest
import tempfile
import os

from app import app, manager, database


class StudentAPITest(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()

        database.filename = self.temp_file.name

        manager.students.clear()

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        manager.students.clear()

        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

        database.filename = "data/students.json"

    def test_home(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_register_student(self):
        response = self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT001",
                "name": "Michael",
                "course": "Mathematics and Computer Science"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_duplicate_student(self):
        self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT001",
                "name": "Michael",
                "course": "Computer Science"
            }
        )

        response = self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT001",
                "name": "Another Student",
                "course": "Mathematics"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_student_fields(self):
        response = self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT002"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_get_students(self):
        self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT003",
                "name": "Peter",
                "course": "Computer Science"
            }
        )

        response = self.client.get("/api/students")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_add_marks(self):
        self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT004",
                "name": "John",
                "course": "Mathematics"
            }
        )

        response = self.client.post(
            "/api/students/JKUAT004/marks",
            json={
                "subject": "Calculus",
                "mark": 85
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_marks(self):
        self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT005",
                "name": "Mary",
                "course": "Mathematics"
            }
        )

        response = self.client.post(
            "/api/students/JKUAT005/marks",
            json={
                "subject": "Calculus",
                "mark": 150
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_update_marks(self):
        self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT006",
                "name": "David",
                "course": "Computer Science"
            }
        )

        self.client.post(
            "/api/students/JKUAT006/marks",
            json={
                "subject": "Programming",
                "mark": 70
            }
        )

        response = self.client.put(
            "/api/students/JKUAT006/marks",
            json={
                "subject": "Programming",
                "mark": 90
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["marks"][0]["mark"], 90)

    def test_delete_student(self):
        self.client.post(
            "/api/students",
            json={
                "admission": "JKUAT007",
                "name": "Grace",
                "course": "Mathematics"
            }
        )

        response = self.client.delete("/api/students/JKUAT007")

        self.assertEqual(response.status_code, 200)

    def test_student_not_found(self):
        response = self.client.get("/api/students/UNKNOWN")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()