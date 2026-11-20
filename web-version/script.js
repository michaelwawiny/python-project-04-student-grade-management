const API_URL = "http://127.0.0.1:5000/api";

let students = [];


// =====================================
// API REQUEST HELPER
// =====================================

async function apiRequest(endpoint, options = {}) {

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
    }

    return data;
}


// =====================================
// LOAD STUDENTS
// =====================================

async function loadStudents() {

    const table = document.getElementById("students-table");

    table.innerHTML = `
        <tr>
            <td colspan="6">Loading students...</td>
        </tr>
    `;

    try {

        students = await apiRequest("/students");

        displayStudents(students);

        updateDashboard();

    } catch (error) {

        table.innerHTML = `
            <tr>
                <td colspan="6">Unable to load students. Check that Flask is running.</td>
            </tr>
        `;

        console.error(error);

    }

}


// =====================================
// CALCULATE AVERAGE
// =====================================

function calculateAverage(marks) {

    if (!marks || marks.length === 0) {
        return 0;
    }

    const total = marks.reduce(
        (sum, item) => sum + Number(item.mark),
        0
    );

    return total / marks.length;

}


// =====================================
// CALCULATE GRADE
// =====================================

function calculateGrade(average) {

    if (average >= 70) return "A";
    if (average >= 60) return "B";
    if (average >= 50) return "C";
    if (average >= 40) return "D";

    return "E";

}


// =====================================
// DISPLAY STUDENTS
// =====================================

function displayStudents(data) {

    const table = document.getElementById("students-table");

    table.innerHTML = "";

    if (data.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="6">No students found.</td>
            </tr>
        `;

        return;

    }

    data.forEach(student => {

        const average = calculateAverage(student.marks);

        const grade = student.marks.length > 0
            ? calculateGrade(average)
            : "-";

        const row = document.createElement("tr");

        const admissionCell = document.createElement("td");
        admissionCell.textContent = student.admission;

        const nameCell = document.createElement("td");
        nameCell.textContent = student.name;

        const courseCell = document.createElement("td");
        courseCell.textContent = student.course;

        const averageCell = document.createElement("td");
        averageCell.textContent = `${average.toFixed(2)}%`;

        const gradeCell = document.createElement("td");
        gradeCell.textContent = grade;

        const actionCell = document.createElement("td");

        const actions = document.createElement("div");
        actions.className = "action-buttons";

        const viewButton = document.createElement("button");
        viewButton.className = "view-button";
        viewButton.textContent = "View";

        viewButton.addEventListener("click", () => {
            viewStudent(student);
        });

        const editButton = document.createElement("button");
        editButton.className = "edit-button";
        editButton.textContent = "Edit Marks";

        editButton.addEventListener("click", () => {
            editStudentMarks(student);
        });

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteStudent(student.admission);
        });

        actions.appendChild(viewButton);
        actions.appendChild(editButton);
        actions.appendChild(deleteButton);

        actionCell.appendChild(actions);

        row.appendChild(admissionCell);
        row.appendChild(nameCell);
        row.appendChild(courseCell);
        row.appendChild(averageCell);
        row.appendChild(gradeCell);
        row.appendChild(actionCell);

        table.appendChild(row);

    });

}


// =====================================
// REGISTER STUDENT
// =====================================

document.getElementById("student-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const admission = document.getElementById(
            "admission-number"
        ).value.trim();

        const name = document.getElementById(
            "student-name"
        ).value.trim();

        const course = document.getElementById(
            "student-course"
        ).value.trim();

        const message = document.getElementById("form-message");

        try {

            await apiRequest("/students", {

                method: "POST",

                body: JSON.stringify({
                    admission,
                    name,
                    course
                })

            });

            message.textContent = "Student registered successfully!";
            message.className = "message success";

            this.reset();

            await loadStudents();

        } catch (error) {

            message.textContent = error.message;
            message.className = "message error";

        }

    }
);


// =====================================
// ADD STUDENT MARKS
// =====================================

document.getElementById("marks-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const admission = document.getElementById(
            "marks-admission"
        ).value.trim();

        const subject = document.getElementById(
            "subject-name"
        ).value.trim();

        const mark = Number(
            document.getElementById("subject-mark").value
        );

        const message = document.getElementById("marks-message");

        if (!Number.isFinite(mark) || mark < 0 || mark > 100) {

            message.textContent = "Marks must be between 0 and 100.";
            message.className = "message error";

            return;

        }

        try {

            await apiRequest(
                `/students/${encodeURIComponent(admission)}/marks`,
                {
                    method: "POST",

                    body: JSON.stringify({
                        subject,
                        mark
                    })
                }
            );

            message.textContent = "Marks saved successfully!";
            message.className = "message success";

            this.reset();

            await loadStudents();

        } catch (error) {

            message.textContent = error.message;
            message.className = "message error";

        }

    }
);


// =====================================
// EDIT STUDENT MARKS
// =====================================

async function editStudentMarks(student) {

    if (student.marks.length === 0) {

        alert("This student has no marks to edit.");

        return;

    }

    const subjects = student.marks
        .map(item => item.subject)
        .join(", ");

    const subject = prompt(
        `Enter the subject to edit:\n${subjects}`
    );

    if (!subject) return;

    const existingMark = student.marks.find(
        item => item.subject.toLowerCase() === subject.trim().toLowerCase()
    );

    if (!existingMark) {

        alert("Subject not found.");

        return;

    }

    const newMark = prompt(
        `Current mark: ${existingMark.mark}\nEnter the new mark:`
    );

    if (newMark === null || newMark.trim() === "") return;

    const mark = Number(newMark);

    if (!Number.isFinite(mark) || mark < 0 || mark > 100) {

        alert("Marks must be between 0 and 100.");

        return;

    }

    try {

        await apiRequest(
            `/students/${encodeURIComponent(student.admission)}/marks`,
            {
                method: "PUT",

                body: JSON.stringify({
                    subject: existingMark.subject,
                    mark
                })
            }
        );

        alert("Marks updated successfully!");

        await loadStudents();

    } catch (error) {

        alert(error.message);

    }

}


// =====================================
// DELETE STUDENT
// =====================================

async function deleteStudent(admission) {

    const confirmed = confirm(
        "Are you sure you want to delete this student?"
    );

    if (!confirmed) return;

    try {

        await apiRequest(
            `/students/${encodeURIComponent(admission)}`,
            {
                method: "DELETE"
            }
        );

        alert("Student deleted successfully.");

        await loadStudents();

    } catch (error) {

        alert(error.message);

    }

}


// =====================================
// VIEW STUDENT PERFORMANCE
// =====================================

function viewStudent(student) {

    const modal = document.getElementById("student-modal");

    const details = document.getElementById("student-details");

    const subjectTable = document.getElementById(
        "subject-performance"
    );

    const totalElement = document.getElementById("student-total");

    const averageElement = document.getElementById("student-average");

    const gradeElement = document.getElementById("student-grade");

    const total = student.marks.reduce(
        (sum, item) => sum + Number(item.mark),
        0
    );

    const average = calculateAverage(student.marks);

    const grade = calculateGrade(average);

    details.innerHTML = "";

    const fields = [
        ["Name", student.name],
        ["Admission", student.admission],
        ["Course", student.course]
    ];

    fields.forEach(([label, value]) => {

        const paragraph = document.createElement("p");

        const strong = document.createElement("strong");

        strong.textContent = `${label}: `;

        paragraph.appendChild(strong);
        paragraph.appendChild(document.createTextNode(value));

        details.appendChild(paragraph);

    });

    subjectTable.innerHTML = "";

    student.marks.forEach(item => {

        const row = document.createElement("tr");

        const subjectCell = document.createElement("td");
        subjectCell.textContent = item.subject;

        const markCell = document.createElement("td");
        markCell.textContent = item.mark;

        const gradeCell = document.createElement("td");
        gradeCell.textContent = calculateGrade(Number(item.mark));

        row.appendChild(subjectCell);
        row.appendChild(markCell);
        row.appendChild(gradeCell);

        subjectTable.appendChild(row);

    });

    if (student.marks.length === 0) {

        subjectTable.innerHTML = `
            <tr>
                <td colspan="3">No marks available.</td>
            </tr>
        `;

    }

    totalElement.textContent = total;

    averageElement.textContent = `${average.toFixed(2)}%`;

    gradeElement.textContent = student.marks.length > 0
        ? grade
        : "-";

    modal.style.display = "flex";

}


// =====================================
// CLOSE PERFORMANCE MODAL
// =====================================

document.getElementById("close-modal").addEventListener(
    "click",
    () => {

        document.getElementById("student-modal").style.display = "none";

    }
);


document.getElementById("student-modal").addEventListener(
    "click",
    event => {

        if (event.target.id === "student-modal") {

            event.target.style.display = "none";

        }

    }
);


document.addEventListener("keydown", event => {

    if (event.key === "Escape") {

        document.getElementById("student-modal").style.display = "none";

    }

});


// =====================================
// SEARCH STUDENTS
// =====================================

document.getElementById("search-input").addEventListener(
    "input",
    function() {

        const searchTerm = this.value.toLowerCase().trim();

        const filteredStudents = students.filter(student => {

            return (
                student.name.toLowerCase().includes(searchTerm) ||
                student.admission.toLowerCase().includes(searchTerm) ||
                student.course.toLowerCase().includes(searchTerm)
            );

        });

        displayStudents(filteredStudents);

    }
);


// =====================================
// UPDATE DASHBOARD STATISTICS
// =====================================

function updateDashboard() {

    document.getElementById("total-students").textContent =
        students.length;

    const studentsWithMarks = students.filter(
        student => student.marks.length > 0
    );

    if (studentsWithMarks.length === 0) {

        document.getElementById("overall-average").textContent = "0%";

        document.getElementById("grade-a-count").textContent = "0";

        document.getElementById("top-grade").textContent = "-";

        document.getElementById("top-student").textContent =
            "No student data available";

        updateGradeDistribution();

        return;

    }

    const averages = studentsWithMarks.map(
        student => calculateAverage(student.marks)
    );

    const overallAverage = averages.reduce(
        (sum, average) => sum + average,
        0
    ) / averages.length;

    const gradeACount = studentsWithMarks.filter(
        student => calculateGrade(
            calculateAverage(student.marks)
        ) === "A"
    ).length;

    const topStudent = studentsWithMarks.reduce(
        (best, current) => {

            return calculateAverage(current.marks) >
                calculateAverage(best.marks)
                ? current
                : best;

        }
    );

    document.getElementById("overall-average").textContent =
        `${overallAverage.toFixed(2)}%`;

    document.getElementById("grade-a-count").textContent =
        gradeACount;

    document.getElementById("top-grade").textContent = "A";

    document.getElementById("top-student").textContent =
        `${topStudent.name} (${calculateAverage(topStudent.marks).toFixed(2)}%)`;

    updateGradeDistribution();

}


// =====================================
// GRADE DISTRIBUTION
// =====================================

function updateGradeDistribution() {

    const container = document.getElementById("grade-distribution");

    const gradeCounts = {
        A: 0,
        B: 0,
        C: 0,
        D: 0,
        E: 0
    };

    const studentsWithMarks = students.filter(
        student => student.marks.length > 0
    );

    studentsWithMarks.forEach(student => {

        const average = calculateAverage(student.marks);

        const grade = calculateGrade(average);

        gradeCounts[grade]++;

    });

    container.innerHTML = "";

    if (studentsWithMarks.length === 0) {

        container.textContent = "No performance data available.";

        return;

    }

    Object.entries(gradeCounts).forEach(([grade, count]) => {

        const percentage = (
            count / studentsWithMarks.length
        ) * 100;

        const row = document.createElement("div");

        row.className = "grade-row";

        const info = document.createElement("div");

        info.className = "grade-info";

        const gradeLabel = document.createElement("span");

        gradeLabel.textContent = `Grade ${grade}`;

        const countLabel = document.createElement("span");

        countLabel.textContent = `${count} students (${percentage.toFixed(1)}%)`;

        info.appendChild(gradeLabel);
        info.appendChild(countLabel);

        const bar = document.createElement("div");

        bar.className = "grade-bar";

        const fill = document.createElement("div");

        fill.className = "grade-fill";

        fill.style.width = `${percentage}%`;

        bar.appendChild(fill);

        row.appendChild(info);
        row.appendChild(bar);

        container.appendChild(row);

    });

}


// =====================================
// REFRESH BUTTON
// =====================================

document.getElementById("refresh-button").addEventListener(
    "click",
    loadStudents
);


// =====================================
// INITIALIZE APPLICATION
// =====================================

loadStudents();