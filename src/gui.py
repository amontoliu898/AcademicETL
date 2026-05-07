import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database import add_grade, average_students, average_subjects, get_grades
from etl import clean_text, import_csv, load_demo_data, valid_grade


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AcademicETL Dashboard")
        self.geometry("1000x650")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self.input_tab = ttk.Frame(self.tabs)
        self.dashboard_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.input_tab, text="Introducción de datos")
        self.tabs.add(self.dashboard_tab, text="Visualización y análisis")

        self.chart_canvas = None

        self.create_input_tab()
        self.create_dashboard_tab()
        self.update_dashboard()

    def create_input_tab(self):
        frame = ttk.Frame(self.input_tab, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Registro académico").pack(anchor="w")

        self.student_input = ttk.Entry(frame)
        self.student_input.pack(fill="x", pady=5)
        self.student_input.insert(0, "")

        self.subject_input = ttk.Entry(frame)
        self.subject_input.pack(fill="x", pady=5)

        self.grade_input = ttk.Entry(frame)
        self.grade_input.pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Guardar calificación",
            command=self.save_grade,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Cargar datos de ejemplo",
            command=self.load_demo,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Importar CSV",
            command=self.load_csv,
        ).pack(fill="x", pady=5)

    def create_dashboard_tab(self):
        frame = ttk.Frame(self.dashboard_tab, padding=10)
        frame.pack(fill="both", expand=True)

        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x")

        self.selector = ttk.Combobox(
            top_frame,
            values=["Media por estudiante", "Media por asignatura"],
            state="readonly",
        )
        self.selector.current(0)
        self.selector.pack(side="left", padx=5)
        self.selector.bind("<<ComboboxSelected>>", lambda event: self.update_dashboard())

        ttk.Button(
            top_frame,
            text="Actualizar",
            command=self.update_dashboard,
        ).pack(side="left", padx=5)

        self.table = ttk.Treeview(
            frame,
            columns=("student", "subject", "grade"),
            show="headings",
        )

        self.table.heading("student", text="Estudiante")
        self.table.heading("subject", text="Asignatura")
        self.table.heading("grade", text="Nota")

        self.table.pack(fill="both", expand=True, pady=10)

        self.chart_frame = ttk.Frame(frame)
        self.chart_frame.pack(fill="both", expand=True)

    def save_grade(self):
        student = clean_text(self.student_input.get())
        subject = clean_text(self.subject_input.get())
        grade = valid_grade(self.grade_input.get())

        if not student or not subject or grade is None:
            messagebox.showerror("Error", "Introduce datos válidos.")
            return

        add_grade(student, subject, grade)

        self.student_input.delete(0, tk.END)
        self.subject_input.delete(0, tk.END)
        self.grade_input.delete(0, tk.END)

        messagebox.showinfo("Correcto", "Registro guardado.")
        self.update_dashboard()

    def load_demo(self):
        load_demo_data()
        messagebox.showinfo("Correcto", "Datos cargados.")
        self.update_dashboard()

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])

        if path:
            import_csv(path)
            messagebox.showinfo("Correcto", "CSV importado.")
            self.update_dashboard()

    def update_dashboard(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for row in get_grades():
            self.table.insert("", tk.END, values=row)

        if self.selector.get() == "Media por estudiante":
            data = average_students()
            title = "Nota media por estudiante"
        else:
            data = average_subjects()
            title = "Nota media por asignatura"

        self.draw_chart(data, title)

    def draw_chart(self, data, title):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        figure = Figure(figsize=(6, 3))
        ax = figure.add_subplot(111)

        if data:
            names = [row[0] for row in data]
            values = [row[1] for row in data]

            ax.bar(names, values)
            ax.set_ylim(0, 10)
            ax.set_ylabel("Nota media")
            ax.set_title(title)
            ax.tick_params(axis="x", rotation=25)
        else:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")

        figure.tight_layout()

        self.chart_canvas = FigureCanvasTkAgg(figure, self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)