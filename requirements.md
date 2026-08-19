ClinicCare Mini EMR
Problem: Clinics record diagnosis code and treatment notes for every consultation. The goal is to create a minimal, secure, and intuitive tool to manage these notes.
Goal: Build a small ClinicCare web app that allows doctors to:
1. Search for ICD-10 diagnosis codes
2. Record a simple patient consultation note with selected diagnosis codes.
3. List past consultation notes.
4. Provide search notes by patient or by diagnosis code
Project Requirements
Backend-using FastAPI
1. Sample Endpoints
GET/diagnosis?search=<term> Search diagnosis codes (from local table or static dataset).
b. POST/consultation Save a consultation note.
c. GET/consultation List all consultation notes.
2. Data
Use a lightweight SQL DB (SQLite/PostgreSQL)
3. Expected Features
a. Input validation with Pydantic.
b. Basic error handling.
Frontend-using Nuxt 3
A page to for Consultations list: Table of past consultations
b. A page for New Consultation Form.
c. A page to provide search and show list
Optional:
Add JWT authentication for doctors and a login page to login