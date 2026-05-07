import pandas as pd

from database import add_grade


def clean_text(text):
    return str(text).strip().title()


def valid_grade(value):
    try:
        grade = float(value)
    except ValueError:
        return None

    if 0 <= grade <= 10:
        return grade

    return None


def load_demo_data():
    data = [
        ("Albert", "Programación", 8.5),
        ("Albert", "Algoritmos", 7.8),
        ("Laura", "Programación", 9.1),
        ("Laura", "Bases De Datos", 8.0),
        ("Marc", "Algoritmos", 6.5),
        ("Marc", "Bases De Datos", 7.2),
        ("Marta", "Estructuras De Datos", 8.4),
        ("Marta", "Programación", 7.6),
    ]

    for student, subject, grade in data:
        add_grade(student, subject, grade)


def import_csv(path):
    data = pd.read_csv(path)
    data = data.drop_duplicates()

    for _, row in data.iterrows():
        student = clean_text(row["student"])
        subject = clean_text(row["subject"])
        grade = valid_grade(row["grade"])

        if student and subject and grade is not None:
            add_grade(student, subject, grade)