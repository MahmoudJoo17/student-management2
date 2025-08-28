from flask import Flask
import sqlite3

app = Flask(__name__)


# ========== Database Setup ==========
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    department TEXT,
                    enrollment_date TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# ========== Routes ==========
@app.route("/")
def index():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        enrollment_date = request.form["enrollment_date"]

        conn = sqlite3.connect("students.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (name, email, phone, department, enrollment_date) VALUES (?, ?, ?, ?, ?)",
                  (name, email, phone, department, enrollment_date))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        enrollment_date = request.form["enrollment_date"]

        c.execute("UPDATE students SET name=?, email=?, phone=?, department=?, enrollment_date=? WHERE id=?",
                  (name, email, phone, department, enrollment_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()
    conn.close()
    return render_template("edit.html", student=student)



if __name__ == "__main__":
    app.run(debug=True)
