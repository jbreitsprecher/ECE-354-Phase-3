import os
import re
from datetime import datetime
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import init_db, db, Assignment, StudyHabit, Syllabus
import PyPDF2
# sec 1 sets up flask
app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# initialize database
init_db(app)



@app.route("/api/health")
def health():
    return {"status": "ok"}



@app.route("/api/assignments", methods=["GET"])
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([a.to_dict() for a in assignments])


@app.route("/api/assignments", methods=["POST"])
def create_assignment():
    data = request.get_json() or {}

    required = ["title", "dueDate"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field '{field}'"}, 400

    assignment = Assignment(
        course_id=data.get("courseId"),
        title=data["title"],
        description=data.get("description"),
        due_date=data["dueDate"],
        assignment_type=data.get("assignmentType"),
        priority=data.get("priority", 1),
        estimated_hours=data.get("estimatedHours")
    )

    db.session.add(assignment)
    db.session.commit()

    return assignment.to_dict(), 201



@app.route("/api/study-habits", methods=["GET"])
def get_study_habits():
    habits = StudyHabit.query.all()
    return jsonify([
        {
            "id": h.id,
            "daysOfWeek": h.days_of_week,
            "startTime": h.start_time,
            "endTime": h.end_time
        }
        for h in habits
    ])

# allows the user to config study routines
@app.route("/api/study-habits", methods=["POST"])
def create_study_habit():
    data = request.get_json() or {}

    required = ["daysOfWeek", "startTime", "endTime"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field '{field}'"}, 400

    habit = StudyHabit(
        user_id=1,
        days_of_week=data["daysOfWeek"],
        start_time=data["startTime"],
        end_time=data["endTime"]
    )

    db.session.add(habit)
    db.session.commit()

    return {
        "id": habit.id,
        "daysOfWeek": habit.days_of_week,
        "startTime": habit.start_time,
        "endTime": habit.end_time
    }, 201


@app.route("/api/study-habits/<int:habit_id>", methods=["DELETE"])
def delete_study_habit(habit_id):
    habit = StudyHabit.query.get(habit_id)
    if not habit:
        return {"error": "Study habit not found"}, 404

    db.session.delete(habit)
    db.session.commit()
    return {"message": "Study habit deleted"}

#this handles the pdf syllabus and uploads and extracts the assignments from the text

@app.route("/api/upload-syllabus", methods=["POST"])
def upload_syllabus():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "Empty filename"}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    syllabus = Syllabus(original_filename=filename)
    db.session.add(syllabus)
    db.session.commit()

    extracted = extract_assignments_from_pdf(filepath)

    for item in extracted:
        a = Assignment(
            course_id=None,
            title=item["title"],
            due_date=item["dueDate"]
        )
        db.session.add(a)

    db.session.commit()

    return {
        "message": "Syllabus uploaded & analyzed",
        "assignmentsExtracted": extracted
    }, 201

#allows the user to paste a link instead of uploading a file
@app.route("/api/import-url", methods=["POST"])
def import_url():
    data = request.get_json() or {}

    if "url" not in data:
        return {"error": "Missing URL"}, 400

    url = data["url"]

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "Failed to download file"}, 400

        filename = "url_import.pdf"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

    except Exception as e:
        return {"error": str(e)}, 500

    syllabus = Syllabus(original_filename=filename)
    db.session.add(syllabus)
    db.session.commit()

    extracted = extract_assignments_from_pdf(filepath)

    for item in extracted:
        a = Assignment(
            course_id=None,
            title=item["title"],
            due_date=item["dueDate"]
        )
        db.session.add(a)

    db.session.commit()

    return {
        "message": "URL PDF imported & analyzed",
        "assignmentsExtracted": extracted
    }, 201

# this scans the syllabus text for dates and sends it to generates

def extract_assignments_from_pdf(filepath):

    text = ""
    try:
        reader = PyPDF2.PdfReader(filepath)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except:
        return []

    assignments = []

    date_patterns = [
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}/\d{1,2}\b"
    ]

    lines = text.split("\n")
    for line in lines:
        cleaned = line.strip()
        if len(cleaned) < 4:
            continue

        for pattern in date_patterns:
            match = re.search(pattern, cleaned)
            if match:
                title = cleaned.replace(match.group(), "").strip()
                due_date = match.group()

                assignments.append({
                    "title": title if title else "Assignment",
                    "dueDate": due_date
                })
                break

    return assignments

#this is just the the end only used for file uploading the file

@app.route("/upload", methods=["POST"])
def upload_file_frontend():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return jsonify({"success": True, "filename": filename}), 200

# creates a downloadable file
@app.route("/generate", methods=["POST"])
def generate_calendar():
    """Generate a basic .ics calendar file from all assignments."""
    output_file = "calendar_output.ics"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_file)

    assignments = Assignment.query.all()

    def to_ics_date(date_str: str):
        """
        Trying to convert various date formats into YYYYMMDD
        Works for:
        - YYYY-MM-DD
        - MM/DD/YYYY
        - MM/DD/YY
        - MM/DD  (current year)
        Returns None if it can't
        """
        if not date_str:
            return None

        s = date_str.strip()

        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
            try:
                dt = datetime.strptime(s, fmt)
                return dt.strftime("%Y%m%d")
            except ValueError:
                continue

        # Trying MM/DD with current year as fallback
        try:
            dt = datetime.strptime(s, "%m/%d")
            dt = dt.replace(year=datetime.now().year)
            return dt.strftime("%Y%m%d")
        except ValueError:
            return None

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//From Syllabus To Schedule//EN",
    ]

    now_utc = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    for a in assignments:
        ics_date = to_ics_date(a.due_date)
        if not ics_date:
            # Skip assignments with unparseable dates
            continue

        uid = f"{a.id}@from-syllabus-to-schedule"

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{now_utc}",
            f"DTSTART;VALUE=DATE:{ics_date}",
            f"DTEND;VALUE=DATE:{ics_date}",
            f"SUMMARY:{a.title}",
            "END:VEVENT",
        ])

    lines.append("END:VCALENDAR")

    # Writing the ICS file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return jsonify({"success": True, "file": output_file})



@app.route("/download/<path:filename>")
def download_output(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )

# runs the flask to development server

if __name__ == "__main__":
    app.run(debug=True)
