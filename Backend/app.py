from flask import Flask, request, jsonify
from flask_cors import CORS
from models import init_db, db, Assignment

app = Flask(__name__)
CORS(app)

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


if __name__ == "__main__":
    app.run(debug=True)
