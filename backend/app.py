from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
import os

from database import init_db
from model import predict_ticket
from router import assign_agent

from router import get_agent_queue, get_all_queues
from router import can_agent_take_ticket, get_next_ticket_for_agent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "tickets.db"
)

app = Flask(__name__,
            template_folder="../frontend", 
            static_folder="../frontend", 
            static_url_path="")
CORS(app)

init_db()

otp_store = {}

@app.route("/")
def home():
    return render_template("login.html")

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

# ================= OTP =================


@app.route("/send_otp", methods=["POST"])
def send_otp():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, email FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # user_email = user[1]



    otp = "123456"
    otp_store[username] = otp

    print("OTP:", otp)

    return jsonify({
        "message": "OTP generated",
        "otp": otp
    })

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    username = data.get("username")
    otp = data.get("otp")

    if otp_store.get(username) != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, email FROM users WHERE username=?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    otp_store.pop(username, None)

    return jsonify({
        "role": user[0],
        "email": user[1]
    })

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if username == "admin" and password == "admin123":
        conn.close()
        return jsonify({"role": "admin", "email": "admin@system.com"})

    cursor.execute(
        "SELECT role, email FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "role": user[0],
            "email": user[1]
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# ================= SIGNUP =================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not password or not email:
        return jsonify({"error": "All fields required"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    cursor.execute(
        "INSERT INTO users (username,email,password,role) VALUES (?,?,?,?)",
        (username, email, password, "customer")
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful"})


# ================= CUSTOMER DASHBOARD =================
@app.route("/customer_stats", methods=["POST"])
def customer_stats():

    data = request.json
    email = data.get("email")

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE email=?", (email,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE email=? AND status='Resolved'", (email,))
    resolved = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) FROM tickets WHERE email=? GROUP BY category", (email,))
    categories = cursor.fetchall()

    cursor.execute("SELECT priority, COUNT(*) FROM tickets WHERE email=? GROUP BY priority", (email,))
    priorities = cursor.fetchall()

    cursor.execute("SELECT status, COUNT(*) FROM tickets WHERE email=? GROUP BY status", (email,))
    status_data = cursor.fetchall()

    conn.close()

    return jsonify({
        "total": total,
        "resolved": resolved,
        "categories": categories,
        "priorities": priorities,
        "status": status_data
    })


# ================= ADMIN DASHBOARD =================
@app.route("/ticket_stats", methods=["GET"])
def ticket_stats():
    try:
        #conn = sqlite3.connect("../database/tickets.db")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'")
        open_tickets = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'")
        resolved_tickets = cursor.fetchone()[0]

        cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
        categories = cursor.fetchall()

        cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
        priorities = cursor.fetchall()

        cursor.execute("SELECT agent_assigned, COUNT(*) FROM tickets GROUP BY agent_assigned")
        agents = cursor.fetchall()

        cursor.execute("""
            SELECT agent_assigned, COUNT(*) 
            FROM tickets 
            WHERE status='Resolved'
            GROUP BY agent_assigned
        """)
        agent_performance = cursor.fetchall()

        cursor.execute("""
            SELECT AVG(
                CASE 
                    WHEN resolved_at IS NOT NULL 
                    THEN (julianday(resolved_at) - julianday(created_at)) * 24
                END
            ) FROM tickets
        """)
        avg_resolution_time = cursor.fetchone()[0] or 0

        conn.close()

        return jsonify({
            "total": total,
            "open": open_tickets,
            "resolved": resolved_tickets,
            "categories": categories,
            "priorities": priorities,
            "agents": agents,
            "agent_performance": agent_performance,
            "avg_resolution_time": avg_resolution_time
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= QUEUE STATUS =================
@app.route("/full_queue_status", methods=["GET"])
def full_queue_status():
    try:
        return jsonify(get_all_queues())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= PROCESS NEXT =================
@app.route("/process_next/<agent>", methods=["POST"])
def process_next(agent):
    try:
        if not can_agent_take_ticket(agent):
            return jsonify({"error": "Agent at max capacity"}), 400

        ticket_id = get_next_ticket_for_agent(agent)

        if not ticket_id:
            return jsonify({"message": "No tickets in queue"})

        return jsonify({"message": f"Ticket {ticket_id} moved to In Progress"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= ✅ NEW: MY TICKETS =================
@app.route("/my_tickets", methods=["POST"])
def my_tickets():
    try:
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email required"}), 400

        #conn = sqlite3.connect("../database/tickets.db")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, subject, category, priority, status, created_at
            FROM tickets
            WHERE email=?
            ORDER BY created_at DESC
        """, (email,))

        rows = cursor.fetchall()
        conn.close()

        return jsonify(rows)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= TICKETS =================
@app.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        #conn = sqlite3.connect("../database/tickets.db")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM tickets
        ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================= SEARCH TICKETS =================
@app.route("/search_tickets", methods=["POST"])
def search_tickets():

    try:

        data = request.json
        keyword = data.get("keyword", "").strip()

        #conn = sqlite3.connect("../database/tickets.db")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if keyword.isdigit():

            cursor.execute("""
            SELECT *
            FROM tickets
            WHERE id = ?
            ORDER BY created_at DESC
            """, (int(keyword),))

        else:

            cursor.execute("""
            SELECT *
            FROM tickets
            WHERE
                email LIKE ?
                OR category LIKE ?
            ORDER BY created_at DESC
            """, (
                f"%{keyword}%",
                f"%{keyword}%"
            ))

        rows = cursor.fetchall()

        conn.close()

        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================= FILTER TICKETS =================
@app.route("/filter_tickets", methods=["POST"])
def filter_tickets():

    try:

        data = request.json

        filter_value = data.get("filter")

        #conn = sqlite3.connect("../database/tickets.db")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if filter_value == "high":

            cursor.execute("""
            SELECT *
            FROM tickets
            WHERE priority='high'
            ORDER BY created_at DESC
            """)

        else:

            cursor.execute("""
            SELECT *
            FROM tickets
            WHERE status=?
            ORDER BY created_at DESC
            """, (filter_value,))

        rows = cursor.fetchall()

        conn.close()

        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ================= UPDATE =================
@app.route("/update_status", methods=["POST"])
def update_status():
    valid_status = ["Open", "In Progress", "Resolved", "Escalated"]

    data = request.json
    ticket_id = data.get("id")
    status = data.get("status")

    if status not in valid_status:
        return jsonify({"error": "Invalid status"}), 400

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()



    cursor.execute(
        "SELECT status FROM tickets WHERE id=?",
        (ticket_id,)
    )

    current_status = cursor.fetchone()[0]

    allowed = {
        "Open": ["In Progress", "Escalated"],
        "In Progress": ["Resolved", "Escalated"],
        "Escalated": ["In Progress", "Resolved"],
        "Resolved": []
    }

    if status not in allowed[current_status]:
        return jsonify({
            "error": f"Cannot move from {current_status} to {status}"
        }), 400




    if status == "Resolved":
        cursor.execute("""
            UPDATE tickets 
            SET status=?, resolved_at=CURRENT_TIMESTAMP 
            WHERE id=?
        """, (status, ticket_id))
    else:
        cursor.execute("UPDATE tickets SET status=? WHERE id=?", (status, ticket_id))

    cursor.execute("""
    INSERT INTO ticket_history (ticket_id, status)
    VALUES (?,?)
    """, (ticket_id, status))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})



@app.route("/submit_ticket", methods=["POST"])
def submit_ticket():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    description = data.get("description")

    text = f"{subject} {description}"

    category, priority, confidence = predict_ticket(text)

    assigned_team = assign_agent(category, priority)

    #conn = sqlite3.connect("../database/tickets.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (name,email,subject,description,category,priority,status,agent_assigned)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        name,
        email,
        subject,
        description,
        category,
        priority,
        "Open",
        assigned_team
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "predicted_category": category,
        "confidence": confidence,
        "priority": priority,
        "assigned_team": assigned_team
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)