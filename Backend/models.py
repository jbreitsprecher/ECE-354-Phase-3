from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Configure the app for SQLite and create all tables."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    name = db.Column(db.String, nullable=True)

    courses = db.relationship("Course", backref="user", lazy=True)
    study_habits = db.relationship("StudyHabit", backref="user", lazy=True)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=True)   # e.g. "ECE 354"
    color = db.Column(db.String, nullable=True)  # for calendar color

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    syllabi = db.relationship("Syllabus", backref="course", lazy=True)
    assignments = db.relationship("Assignment", backref="course", lazy=True)


class Syllabus(db.Model):
    __tablename__ = "syllabi"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    original_filename = db.Column(db.String, nullable=True)
    # later: you can add a file path or raw text


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    # store as ISO string for now, e.g. "2025-10-20"
    due_date = db.Column(db.String, nullable=False)

    assignment_type = db.Column(db.String, nullable=True)  # exam, hw, quiz, project
    priority = db.Column(db.Integer, default=1)            # 1=low, 2=med, 3=high
    estimated_hours = db.Column(db.Float, nullable=True)


class StudyHabit(db.Model):
    __tablename__ = "study_habits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # e.g. "Mon,Wed,Fri"
    days_of_week = db.Column(db.String, nullable=False)

    # "HH:MM" strings
    start_time = db.Column(db.String, nullable=False)  # "18:00"
    end_time = db.Column(db.String, nullable=False)    # "20:00"
