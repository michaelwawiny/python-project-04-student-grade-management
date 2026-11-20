# Student Grade Management System

A Python-based Student Grade Management System with a browser-based
dashboard built using HTML, CSS and JavaScript.

The application uses Flask to connect the frontend to the Python
backend and JSON for data persistence.

## Features

- Register students
- View student records
- Search students
- Add student marks
- Update existing marks
- Delete student records
- Calculate total marks
- Calculate average marks
- Automatically assign grades
- Identify top-performing students
- Generate grade distribution reports
- Store student records using JSON
- REST API integration

## Technologies Used

### Backend
- Python
- Flask
- Flask-CORS
- JSON

### Frontend
- HTML5
- CSS3
- JavaScript

### Testing
- Python unittest

## Project Structure

```text
project-04-student-grade-management/
│
├── main.py
├── student.py
├── grade_manager.py
├── database.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── students.json
│
├── tests/
│   ├── test_student.py
│   └── test_api.py
│
└── web-version/
    ├── index.html
    ├── style.css
    └── script.js