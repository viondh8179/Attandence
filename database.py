import sqlite3
import os
from datetime import datetime

DB_PATH = "data/attendance.db"

# ─────────────────────────────
def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ─────────────────────────────
def initialize_db():
    conn = get_connection()
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# ─────────────────────────────
# STUDENTS (CRUD)
def add_student(name, email, phone):
    conn = get_connection()
    conn.execute("INSERT INTO students(name,email,phone) VALUES (?,?,?)",
                 (name, email, phone))
    conn.commit()
    conn.close()

def update_student(student_id, name, email, phone):
    conn = get_connection()
    conn.execute("""
        UPDATE students
        SET name=?, email=?, phone=?
        WHERE student_id=?
    """, (name, email, phone, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()

# ─────────────────────────────
# COURSES
def add_course(course_name):
    conn = get_connection()
    conn.execute("INSERT INTO courses(course_name) VALUES (?)", (course_name,))
    conn.commit()
    conn.close()

# ─────────────────────────────
# ENROLLMENT (FIXED FEATURE)
def enroll_student(student_id, course_id):
    conn = get_connection()
    conn.execute("INSERT INTO enrollments(student_id,course_id) VALUES (?,?)",
                 (student_id, course_id))
    conn.commit()
    conn.close()

# ─────────────────────────────
# ATTENDANCE
def mark_attendance(student_id, course_id, date, status):
    conn = get_connection()
    conn.execute("""
        INSERT INTO attendance(student_id,course_id,date,status)
        VALUES (?,?,?,?)
    """, (student_id, course_id, date, status))
    conn.commit()
    conn.close()

# ─────────────────────────────
# HISTORY (INNER JOIN)
def get_attendance_history():
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.name, c.course_name, a.date, a.status
        FROM attendance a
        INNER JOIN students s ON a.student_id = s.student_id
        INNER JOIN courses c ON a.course_id = c.course_id
        ORDER BY a.date DESC
    """).fetchall()
    conn.close()
    return rows

# ─────────────────────────────
# PERCENTAGE
def attendance_percentage(student_id):
    conn = get_connection()

    total = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE student_id=?",
        (student_id,)
    ).fetchone()[0]

    present = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",
        (student_id,)
    ).fetchone()[0]

    conn.close()
    return (present / total * 100) if total else 0

# ─────────────────────────────
# ABSENT REPORT
def absent_students():
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.name, c.course_name, a.date
        FROM attendance a
        INNER JOIN students s ON a.student_id = s.student_id
        INNER JOIN courses c ON a.course_id = c.course_id
        WHERE a.status='Absent'
    """).fetchall()
    conn.close()
    return rows

# ─────────────────────────────
# LEFT JOIN REPORT (NEW FIX)
def course_wise_report():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.course_name, s.name, a.status
        FROM courses c
        LEFT JOIN attendance a ON c.course_id = a.course_id
        LEFT JOIN students s ON a.student_id = s.student_id
    """).fetchall()
    conn.close()
    return rows

# ─────────────────────────────
# LOW ATTENDANCE (<75%)
def low_attendance_students():
    conn = get_connection()
    rows = conn.execute("""
        SELECT student_id,
        (SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)*100.0 / COUNT(*)) as percent
        FROM attendance
        GROUP BY student_id
        HAVING percent < 75
    """).fetchall()
    conn.close()
    return rows

# ─────────────────────────────
# MONTHLY SUMMARY
def monthly_summary(month):
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.name,
               COUNT(*) as total,
               SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present,
               SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END) as absent
        FROM attendance a
        INNER JOIN students s ON a.student_id = s.student_id
        WHERE strftime('%Y-%m', a.date) = ?
        GROUP BY a.student_id
    """, (month,)).fetchall()
    conn.close()
    return rows