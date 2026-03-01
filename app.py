from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)

# ----------------------------
# Database Connection
# ----------------------------
def get_db():
    conn = sqlite3.connect("database.db", timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# Create Table
# ----------------------------
def create_table():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT NOT NULL,
        email TEXT,
        service TEXT,
        message TEXT,
        status TEXT DEFAULT 'New',
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

create_table()


# ----------------------------
# Pages
# ----------------------------
@app.route("/")
def form():
    return render_template("form.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


# ----------------------------
# POST API - Save Lead
# ----------------------------
@app.route("/api/leads", methods=["POST"])
def save_lead():

    data = request.get_json()

    # 🔴 IMPORTANT FIX
    if not data:
        return jsonify({"error": "No data received"}), 400

    name = data.get("name", "").strip()
    mobile = data.get("mobile", "").strip()
    email = data.get("email", "").strip()
    service = data.get("service", "")
    message = data.get("message", "")

    # ----------------------------
    # Validation
    # ----------------------------

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if not re.fullmatch(r"\d{10}", mobile):
        return jsonify({"error": "Mobile number must be exactly 10 digits"}), 400

    if email:
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
            return jsonify({"error": "Email must end with @gmail.com"}), 400

    # ----------------------------
    # Insert into DB
    # ----------------------------
    try:
        conn = get_db()

        conn.execute("""
        INSERT INTO leads(name,mobile,email,service,message,created_at)
        VALUES(?,?,?,?,?,?)
        """, (
            name,
            mobile,
            email,
            service,
            message,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Lead saved successfully"}), 200


# ----------------------------
# GET Leads
# ----------------------------
@app.route("/api/leads")
def get_leads():

    conn = get_db()
    leads = conn.execute(
        "SELECT * FROM leads ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in leads])


# ----------------------------
# UPDATE Status
# ----------------------------
@app.route("/api/leads/<int:id>", methods=["PUT"])
def update_status(id):

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    status = data.get("status", "")

    conn = get_db()
    conn.execute(
        "UPDATE leads SET status=? WHERE id=?",
        (status, id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated"})


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)