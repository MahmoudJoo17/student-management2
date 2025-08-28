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


if __name__ == "__main__":
    app.run(debug=True)
