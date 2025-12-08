# From Syllabus to Schedule
An interactive scheduling tool that extracts assignment deadlines from a student's syllabus and generates a smart, 
organized schedule.

# Overview
From Syllabus to Schedule is a student productivity application designed to simplify academic planning.  
Students upload their course syllabus PDF, and the system:

Extracts assignment names and due dates
Stores them in a local database
Allows entry of study habits
Generates an `.ics` calendar file importable into Google Calendar, Outlook, etc.
Displays a simple in-browser monthly calendar interface

# Features Implemented

# Backend (Flask + SQLite)
Upload syllabus PDF and extract assignments using `PyPDF2` + regex

REST API for:
    Assignments (GET, POST)
    Study habits (GET, POST, DELETE)
    Health check endpoint
Generate `.ics` calendar containing assignment events
Store all data using SQLAlchemy ORM

# Frontend (HTML + CSS + JavaScript)
Upload interface for syllabus files
Study habits test page
Simple calendar UI with month navigation 
Button to generate and download calendar file

# Technology Stack
Backend:
Python
Flask
Flask-CORS
SQLAlchemy (SQLite database)
PyPDF2 for PDF extraction

Frontend:
HTML
CSS
JavaScript

Tools:
IntelliJ / VS Code
Git & GitHub for version control
Local virtual environment for Python dependencies

# Project Structure
ECE-354-Phase-3/

Backend/
    app.py # Main Flask application
    models.py # SQLAlchemy ORM models
    requirements.txt # Python dependencies
    uploads/ # Uploaded syllabi + generated ICS files
    calendar_output.ics # Example generated file
Frontend/
    index.html # Main UI
    study_hab.html # Study habits tester
    styles.css # UI styling
    app.js # Calendar + frontend logic
README.md # (This file)

# How to Run the Project (Backend)

# 1. Navigate to the Backend folder

cd Backend

# 2. Activate the virtual environment
venv\Scripts\activate   # Windows

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Run the Flask server
python app.py


The backend will run at:
http://127.0.0.1:5000

# How to Run the Frontend

# Open these files directly in your browser:

Frontend/index.html

Frontend/study_hab.html

# API Endpoints
Endpoint	            Description
/api/health	            Server health check
/api/assignments	    Retrieve all assignments
/api/assignments	    Add a new assignment
/api/study-habits	    Retrieve study habits
/api/study-habits	    Create a study habit
/api/study-habits/<id>	Delete a study habit
/api/upload-syllabus	Upload PDF syllabus & extract assignments
📅 ICS Calendar Generation

Click Generate Calendar inside the frontend UI.
The system creates an .ics file inside:
Backend/uploads/


You can import this file into:

Google Calendar
Outlook
Apple Calendar
Windows Calendar

Each assignment from the database becomes an event in the .ics file.

# Known Issues / Limitations

PDF extraction depends on syllabus formatting
Calendar UI does not yet display assignment events
No user accounts or login system
Smart notifications not fully implemented
Limited support for unusual date formats
Designed as a single-user prototype

# Credits

Developed by Joshua Breitsprecher & Hadrian Gonzalez
Course: ECE 354 – Software Engineering Capstone
Instructor: Professor Mohsen

Libraries used:
Flask
SQLAlchemy
PyPDF2
HTML/CSS/JavaScript

# License

This project is for educational and academic use only.