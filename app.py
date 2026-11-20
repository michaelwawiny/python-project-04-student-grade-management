import math

from flask import Flask, request, jsonify
from flask_cors import CORS

from grade_manager import GradeManager
from database import Database


# =====================================
# APPLICATION CONFIGURATION
# =====================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500"
            ]
        }
    }
)

database = Database()
manager = GradeManager()


# =====================================
# LOAD DATABASE
# =====================================

def load_data():

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


load_data()


# =====================================
# SAVE DATABASE
# =====================================

def save_data():

    database.save_students(
        manager.get_all_students()
    )


# =====================================
# INPUT VALIDATION
# =====================================

def get_request_data():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None

    return data


def validate_text(value, field, max_length=100):

    if not isinstance(value, str):
        raise ValueError(f"{field} must be text.")

    value = value.strip()

    if not value:
        raise ValueError(f"{field} is required.")

    if len(value) > max_length:
        raise ValueError(
            f"{field} must not exceed {max_length} characters."
        )

    return value


def validate_mark(value):

    if isinstance(value, bool):
        raise ValueError("Marks must be a valid number.")

    try:
        mark = float(value)
    except (ValueError, TypeError):
        raise ValueError("Marks must be a valid number.")

    if not math.isfinite(mark):
        raise ValueError("Marks must be a finite number.")

    if not 0 <= mark <= 100:
        raise ValueError("Marks must be between 0 and 100.")

    return mark


# =====================================
# STUDENT SERIALIZATION
# =====================================

def student_to_json(student):

    return {
        "admission": student.admission_number,
        "name": student.name,
        "course": student.course,
        "marks": [
            {
                "subject": subject,
                "mark": mark
            }
            for subject, mark in student.marks.items()
        ],
        "average": round(
            student.calculate_average(), 2
        ),
        "grade": student.get_grade()
    }


# =====================================
# HOME ROUTE
# =====================================

@app.route("/")
def home():

    return jsonify({
        "message": "Student Grade Management API is running."
    })


# =====================================
# GET ALL STUDENTS
# =====================================

@app.route("/api/students", methods=["GET"])
def get_students():

    students = manager.get_all_students()

    return jsonify([
        student_to_json(student)
        for student in students
    ])


# =====================================
# REGISTER STUDENT
# =====================================

@app.route("/api/students", methods=["POST"])
def add_student():

    data = get_request_data()

    if data is None:
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    try:

        admission = validate_text(
            data.get("admission"),
            "Admission number",
            30
        )

        name = validate_text(
            data.get("name"),
            "Name",
            100
        )

        course = validate_text(
            data.get("course"),
            "Course",
            100
        )

        student = manager.add_student(
            admission,
            name,
            course
        )

        save_data()

        return jsonify(
            student_to_json(student)
        ), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# =====================================
# GET SINGLE STUDENT
# =====================================

@app.route("/api/students/<admission>", methods=["GET"])
def get_student(admission):

    student = manager.get_student(admission)

    if student is None:

        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify(
        student_to_json(student)
    )


# =====================================
# ADD STUDENT MARKS
# =====================================

@app.route(
    "/api/students/<admission>/marks",
    methods=["POST"]
)
def add_marks(admission):

    data = get_request_data()

    if data is None:
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    student = manager.get_student(admission)

    if student is None:

        return jsonify({
            "error": "Student not found."
        }), 404

    try:

        subject = validate_text(
            data.get("subject"),
            "Subject",
            100
        )

        mark = validate_mark(
            data.get("mark")
        )

        if subject.lower() in {
            existing.lower()
            for existing in student.marks
        }:

            return jsonify({
                "error": "Marks for this subject already exist. Use the update option."
            }), 400

        manager.update_student_mark(
            admission,
            subject,
            mark
        )

        save_data()

        return jsonify(
            student_to_json(student)
        ), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# =====================================
# UPDATE STUDENT MARKS
# =====================================

@app.route(
    "/api/students/<admission>/marks",
    methods=["PUT"]
)
def update_marks(admission):

    data = get_request_data()

    if data is None:
        return jsonify({
            "error": "A valid JSON object is required."
        }), 400

    student = manager.get_student(admission)

    if student is None:

        return jsonify({
            "error": "Student not found."
        }), 404

    try:

        subject = validate_text(
            data.get("subject"),
            "Subject",
            100
        )

        existing_subject = next(
            (
                existing
                for existing in student.marks
                if existing.lower() == subject.lower()
            ),
            None
        )

        if existing_subject is None:

            return jsonify({
                "error": "Subject not found."
            }), 404

        mark = validate_mark(
            data.get("mark")
        )

        student.add_mark(
            existing_subject,
            mark
        )

        save_data()

        return jsonify(
            student_to_json(student)
        )

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# =====================================
# DELETE STUDENT
# =====================================

@app.route(
    "/api/students/<admission>",
    methods=["DELETE"]
)
def delete_student(admission):

    try:

        manager.delete_student(admission)

        save_data()

        return jsonify({
            "message": "Student deleted successfully."
        })

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )