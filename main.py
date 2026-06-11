from database import *
import datetime

initialize_db()

# ─────────────────────────────
def menu():
    print("\n==============================")
    print("🧑‍🎓 Student Attendance System")
    print("==============================")
    print("1. Student Registration")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. Course Creation")
    print("5. Enroll Student")
    print("6. Mark Attendance")
    print("7. Attendance History")
    print("8. Attendance Percentage")
    print("9. Absent Student Report")
    print("10. Course-wise Report")
    print("11. Monthly Summary")
    print("12. Low Attendance (<75%)")
    print("13. Exit")

# ─────────────────────────────
while True:
    menu()
    choice = input("Enter choice: ")

    # ── Student Registration ──
    if choice == "1":
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        add_student(name, email, phone)
        print("✅ Student Registered")

    # ── Update Student ──
    elif choice == "2":
        sid = input("Student ID: ")
        name = input("New Name: ")
        email = input("New Email: ")
        phone = input("New Phone: ")
        update_student(sid, name, email, phone)
        print("✅ Student Updated")

    # ── Delete Student ──
    elif choice == "3":
        sid = input("Student ID: ")
        delete_student(sid)
        print("❌ Student Deleted")

    # ── Course Creation ──
    elif choice == "4":
        course = input("Course Name: ")
        add_course(course)
        print("✅ Course Created")

    # ── Enroll Student ──
    elif choice == "5":
        sid = input("Student ID: ")
        cid = input("Course ID: ")
        enroll_student(sid, cid)
        print("✅ Student Enrolled")

    # ── Mark Attendance ──
    elif choice == "6":
        sid = input("Student ID: ")
        cid = input("Course ID: ")
        status = input("Status (Present/Absent): ")
        date = str(datetime.date.today())
        mark_attendance(sid, cid, date, status)
        print("✅ Attendance Marked")

    # ── Attendance History ──
    elif choice == "7":
        rows = get_attendance_history()
        print("\n--- Attendance History ---")
        for r in rows:
            print(r["name"], "|", r["course_name"], "|", r["date"], "|", r["status"])

    # ── Attendance Percentage ──
    elif choice == "8":
        sid = input("Student ID: ")
        percent = attendance_percentage(sid)
        print(f"📊 Attendance: {percent:.2f}%")

    # ── Absent Report ──
    elif choice == "9":
        rows = absent_students()
        print("\n--- Absent Students ---")
        for r in rows:
            print(r["name"], "|", r["course_name"], "|", r["date"])

    # ── Course-wise Report ──
    elif choice == "10":
        rows = course_wise_report()
        print("\n--- Course-wise Report ---")
        for r in rows:
            print(r["course_name"], "|", r["name"], "|", r["status"])

    # ── Monthly Summary ──
    elif choice == "11":
        month = input("Enter month (YYYY-MM): ")
        rows = monthly_summary(month)

        print("\n--- Monthly Summary ---")
        for r in rows:
            print(
                r["name"],
                "| Total:", r["total"],
                "| Present:", r["present"],
                "| Absent:", r["absent"]
            )

    # ── Low Attendance ──
    elif choice == "12":
        rows = low_attendance_students()

        print("\n--- Students Below 75% ---")
        for r in rows:
            print("Student ID:", r["student_id"], "| Attendance:", round(r["percent"], 2), "%")

    # ── Exit ──
    elif choice == "13":
        print("👋 Goodbye")
        break

    else:
        print("❌ Invalid Choice")