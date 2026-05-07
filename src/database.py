import sqlite3

DB_NAME = "academic_etl.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            grade REAL NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    conn.commit()
    conn.close()


def add_student(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def add_subject(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def get_id(table, name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def add_grade(student, subject, grade):
    add_student(student)
    add_subject(subject)

    student_id = get_id("students", student)
    subject_id = get_id("subjects", subject)

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
        (student_id, subject_id, grade),
    )
    conn.commit()
    conn.close()


def get_grades():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.name, subjects.name, grades.grade
        FROM grades
        JOIN students ON grades.student_id = students.id
        JOIN subjects ON grades.subject_id = subjects.id
        ORDER BY students.name
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def average_students():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.name, ROUND(AVG(grades.grade), 2)
        FROM grades
        JOIN students ON grades.student_id = students.id
        GROUP BY students.name
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def average_subjects():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subjects.name, ROUND(AVG(grades.grade), 2)
        FROM grades
        JOIN subjects ON grades.subject_id = subjects.id
        GROUP BY subjects.name
    """)

    data = cursor.fetchall()
    conn.close()
    return data