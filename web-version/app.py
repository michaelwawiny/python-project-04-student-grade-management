from flask import Flask, request, jsonify
from flask_cors import CORS

from grade_manager import GradeManager
from database import Database

app = Flask(__name__)
CORS(app)

database = Database()
manager = GradeManager()


# =====================================
# LOAD EXISTING STUDENTS
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
# SAVE DATA
# =====================================

def save_data():

    database.save_students(manager.get_all_students())


# =====================================
# CONVERT STUDENT TO JSON
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
        "average": round(student.calculate_average(), 2),
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

    data = request.get_json(silent=True) or {}

    admission = str(data.get("admission", "")).strip()
    name = str(data.get("name", "")).strip()
    course = str(data.get("course", "")).strip()

    if not admission or not name or not course:

        return jsonify({
            "error": "All fields are required."
        }), 400

    try:

        student = manager.add_student(
            admission,
            name,
            course
        )

        save_data()

        return jsonify(student_to_json(student)), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# =====================================
# GET ONE STUDENT
# =====================================

@app.route("/api/students/<admission>", methods=["GET"])
def get_student(admission):

    student = manager.get_student(admission)

    if student is None:

        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify(student_to_json(student))


# =====================================
# ADD STUDENT MARKS
# =====================================

@app.route(
    "/api/students/<admission>/marks",
    methods=["POST"]
)
def add_marks(admission):

    data = request.get_json(silent=True) or {}

    subject = str(data.get("subject", "")).strip()
    mark = data.get("mark")

    if not subject:

        return jsonify({
            "error": "Subject is required."
        }), 400

    try:

        mark = float(mark)

        manager.update_student_mark(
            admission,
            subject,
            mark
        )

        save_data()

        student = manager.get_student(admission)

        return jsonify(student_to_json(student))

    except (ValueError, TypeError) as error:

        return jsonify({
            "error": str(error)
        }), 400


# =====================================
# UPDATE EXISTING MARK
# =====================================

@app.route(
    "/api/students/<admission>/marks",
    methods=["PUT"]
)
def update_marks(admission):

    data = request.get_json(silent=True) or {}

    subject = str(data.get("subject", "")).strip()
    mark = data.get("mark")

    student = manager.get_student(admission)

    if student is None:

        return jsonify({
            "error": "Student not found."
        }), 404

    if not subject or subject not in student.marks:

        return jsonify({
            "error": "Subject not found."
        }), 404

    try:

        mark = float(mark)

        if not 0 <= mark <= 100:

            return jsonify({
                "error": "Marks must be between 0 and 100."
            }), 400

        student.add_mark(subject, mark)

        save_data()

        return jsonify(student_to_json(student))

    except (ValueError, TypeError) as error:

        return jsonify({
            "error": str(error)
        }), 400


# =====================================
# DELETE STUDENT
# =====================================

@app.route("/api/students/<admission>", methods=["DELETE"])
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
        debug=True
    )