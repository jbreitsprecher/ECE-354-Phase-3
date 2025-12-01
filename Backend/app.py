import os
import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import init_db, db, Assignment

app = Flask(__name__)
CORS(app)

# upload

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# initialize database + create tables
init_db(app)


@app.route("/api/health")
def health():
    return {"status": "ok"}


# GET /api/assignments  -> list all assignments
@app.route("/api/assignments", methods=["GET"])
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([a.to_dict() for a in assignments])


# POST /api/assignments -> create a new assignment
@app.route("/api/assignments", methods=["POST"])
def create_assignment():
    data = request.get_json() or {}

    # Simple validation
    required = ["title", "dueDate"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field '{field}'"}, 400

    assignment = Assignment(
        course_id=data.get("courseId"),         # optional for now
        title=data["title"],
        description=data.get("description"),
        due_date=data["dueDate"],
        assignment_type=data.get("assignmentType"),
        priority=data.get("priority", 1),
        estimated_hours=data.get("estimatedHours"),
    )

    db.session.add(assignment)
    db.session.commit()

    return assignment.to_dict(), 201

#pdf upload
@app.route("/api/upload-syllabus" , methods = ["POST"])
def upload_syllabus():
    if "file" not in request.files:
        return{"error": "No file uploaded"}, 400

    file = request.files ["file"]

    if file.filename== "":
        return{"error": "Empty filename"}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config ["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    syllabus = Syllabus (original_filename =filename)
    db.session.add(syllabus)
    db.session.commit()
# this is for extract and analyze
extracted = extract_assignments_from_pdf(filepath)

# calls to save the assignments
for item in extracted:
    a = Assignment(
    course_id = None,
    title = item ["title"],
    due_date=item ["dueDate"],

    )
    db.session.add(a)
    db.session.commit()

    return{
    "message": "Syllabus uploaded & analyzed",
    "assignmentsExtracted": extracted
    }, 201


#this part is for SYL from a Url

@app.route("/api/import-url", methods=["POST"])
def import_url():
    data = request.get_json()
    if "url" not in data:
        return{"error" : "Missing URL"}, 400

   url = data ["url"]
# download pdf
   try:
       response = requests.get (url)
       if response.status_code != 200:
           return {"error": "Failed to download file"}, 400
# save for temp
    filename = "url_import.pdf"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

except Exception as e:
    return {"error" : str(e)}, 500


   syllabus = Syllabus(original_filename=filename)
       db.session.add(syllabus)
       db.session.commit()

       # analyze PDF
       extracted = extract_assignments_from_pdf(filepath)

       # insert extracted assignments
       for item in extracted:
           a = Assignment(
               course_id=None,
               title=item["title"],
               due_date=item["dueDate"],
           )
           db.session.add(a)

       db.session.commit()

       return {
           "message": "URL PDF imported & analyzed",
           "assignmentsExtracted": extracted


       }, 201


def extract_assignments_from_pdf(filepath)
"""
SUPER sinmple assignment extractor.
Looks for:
    -dates (Feb 20, 2/12/25, Apr.5)
    -lines with assignments names before the date
"""
try:
    import PyPDF2
    expect ImportError:
    return[]

text = ""
try:
    reader = PyPDF2.PdfReader(filepath)
    for page in reader.pages:
        text += page.extract_text() + "\n"
except:
    return[]

assignments = []

#this detects due dates

date_patterns = [
r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}/\d{1,2}\b"
]
lines = text.split("\n")
for line in lines:
    cleaned = line.strip()
    if len(cleaned)<4:
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





if __name__ == "__main__":
    app.run(debug=True)
