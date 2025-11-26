from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import mysql.connector
from datetime import date, datetime
from config import Config
from functools import wraps
import pandas as pd
import google.generativeai as genai
import re
import os
import json
from dotenv import load_dotenv
import time

# -------------------------------------------------
# App & extensions
# -------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Session configuration for security and timeout
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# ---------- File upload settings for test questions ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTION_UPLOAD_SUBDIR = os.path.join("static", "uploads", "questions")
QUESTION_UPLOAD_FOLDER = os.path.join(BASE_DIR, QUESTION_UPLOAD_SUBDIR)

os.makedirs(QUESTION_UPLOAD_FOLDER, exist_ok=True)

app.config["QUESTION_UPLOAD_FOLDER"] = QUESTION_UPLOAD_FOLDER

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif"}
ALLOWED_AUDIO_EXT = {"mp3", "wav", "ogg"}

load_dotenv()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Your session has expired. Please log in again."
login_manager.login_message_category = "info"
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
ADMIN_PASSKEY = "child1234"

# -------------- GEMINI + BENCHMARK SETUP --------------
genai.configure(api_key=app.config["GOOGLE_API_KEY"])

BENCHMARK_PATH = "static/data/developmental_milestones.csv"
benchmark_df = pd.read_csv(BENCHMARK_PATH)
benchmark_df.columns = [c.strip().capitalize() for c in benchmark_df.columns]


# -------------------------------------------------
# DB helper
# -------------------------------------------------
def get_db_conn():
    return mysql.connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASS"],
        database=app.config["DB_NAME"],
    )


# -------------------------------------------------
# User model for Flask-Login
# -------------------------------------------------
class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, email, role FROM users WHERE id = %s", (user_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row["id"], row["name"], row["email"], row["role"])
    return None


# Session timeout handler
@app.before_request
def before_request():
    """Refresh session activity timestamp on each request"""
    if current_user.is_authenticated:
        session.modified = True


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def is_strong_password(password: str) -> bool:
    if not password:
        return False
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,})"
    return re.search(pattern, password) is not None

def is_valid_name(name: str) -> bool:
    """
    Validate that a name contains only alphabet letters and spaces.
    Returns True if valid, False otherwise.
    """
    if not name or not name.strip():
        return False
    # Allow only letters (any language) and spaces
    pattern = r"^[A-Za-z\s]+$"
    return re.match(pattern, name.strip()) is not None

def normalize_role(role):
    if not role:
        return None
    normalized = str(role).strip().lower()
    aliases = {
        "administrator": "admin",
        "admin": "admin",
        "parent": "parent",
    }
    return aliases.get(normalized)


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            normalized_user_role = (
                normalize_role(current_user.role)
                if current_user.is_authenticated
                else None
            )
            normalized_roles = [normalize_role(r) for r in roles]

            if (
                not current_user.is_authenticated
                or normalized_user_role not in normalized_roles
            ):
                flash("You don't have access to that page.", "danger")
                return redirect(url_for("login"))
            return f(*args, **kwargs)

        return wrapped

    return wrapper



def save_question_media(file_storage, test_id, index):
    """
    Save uploaded file for a question and return (media_type, media_path).
    media_path is relative to static/, e.g. 'uploads/questions/xxx.png'
    """
    if not file_storage or not file_storage.filename:
        return None, None

    filename = file_storage.filename
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext in ALLOWED_IMAGE_EXT:
        media_type = "image"
    elif ext in ALLOWED_AUDIO_EXT:
        media_type = "audio"
    else:
        # unsupported extension
        return None, None

    safe_name = f"test{test_id}_q{index+1}_{int(time.time())}.{ext}"
    full_path = os.path.join(app.config["QUESTION_UPLOAD_FOLDER"], safe_name)

    file_storage.save(full_path)

    # store path relative to static/
    media_path = os.path.join("uploads", "questions", safe_name).replace("\\", "/")
    return media_type, media_path




# -------------------------------------------------
# AUTH
# -------------------------------------------------
@app.route("/register")
def register_redirect():
    return redirect(url_for("register_select"))


@app.route("/register/select")
def register_select():
    return render_template("register_select.html")


@app.route("/register/parent", methods=["GET", "POST"])
def register_parent():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")

        if not all([name, email, password, confirm_password]):
            flash("Please fill all fields", "warning")
            return redirect(url_for('register_parent'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register_parent"))

        if not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("register_parent"))
        
        if not is_strong_password(password):
            flash("Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, and one symbol.", "warning")
            return redirect(url_for('register_parent'))

        # Validate name contains only alphabet letters
        if not is_valid_name(name):
            flash("Name must contain only alphabet letters and spaces.", "danger")
            return redirect(url_for("register_parent"))
        
        # Check for duplicate email
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("register_parent"))

        cursor.close()
        conn.close()

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, 'parent')
            """,
            (name, email, hashed_password),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Parent account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register_parent.html")


@app.route("/register/admin", methods=["GET", "POST"])
def register_admin():
    if request.method == "POST":
        key = request.form.get("admin_passkey", "").strip()
        if key != ADMIN_PASSKEY:
            flash("Invalid admin key.", "danger")
            return redirect(url_for("register_admin"))

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")

        if not all([name, email, password, confirm_password, key]):
            flash("Please fill all fields", "warning")
            return redirect(url_for('register_admin'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register_admin"))
        
        # Check for duplicate email
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("register_admin"))

        cursor.close()
        conn.close()

        # Validate name contains only alphabet letters
        if not is_valid_name(name):
            flash("Name must contain only alphabet letters and spaces.", "danger")
            return redirect(url_for("register_admin"))
        
        if not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("register_admin"))
        
        if not is_strong_password(password):
            flash("Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, and one symbol.", "warning")
            return redirect(url_for('register_admin'))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, 'admin')
            """,
            (name, email, hashed_password),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Admin account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register_admin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        remember_me = request.form.get("remember_me") == "on"

        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, email, password, role FROM users WHERE email = %s",
            (email,),
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(
                user["id"], user["name"], user["email"], user["role"]
            )
            # Set session as permanent to enable timeout
            session.permanent = True
            # Login user with remember_me option
            login_user(user_obj, remember=remember_me)
            flash("Logged in successfully.", "success")

            if normalize_role(user_obj.role) == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("profile"))

        flash("Invalid credentials.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


def send_reset_email(to_email, token):
    reset_url = url_for("reset_password", token=token, _external=True)
    msg = Message("ChildGrowth Insights - Password Reset", recipients=[to_email])

    msg.body = f"""
To reset your password for ChildGrowth Insights, click the link below (valid for 1 hour):

{reset_url}

If you didn't request this, you can safely ignore this email.
"""

    msg.html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 0;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding: 30px 0;">
          <table width="600" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <tr>
              <td style="background: #0d6efd; padding: 20px; text-align: center; color: #ffffff; font-size: 22px; font-weight: bold;">
                ChildGrowth Insights
              </td>
            </tr>
            <tr>
              <td style="padding: 30px; color: #333333; font-size: 16px;">
                <p>Hello,</p>
                <p>We received a request to reset your password for your <strong>ChildGrowth Insights</strong> account.</p>
                <p>Click the button below to reset it. This link is valid for <strong>1 hour</strong>:</p>
                <p style="text-align: center; margin: 30px 0;">
                  <a href="{reset_url}" style="background: #0d6efd; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Reset Password
                  </a>
                </p>
                <p>If you did not request this, you can safely ignore this email.</p>
                <p>Best regards,<br><strong>ChildGrowth Insights Team</strong></p>
              </td>
            </tr>
            <tr>
              <td style="background: #f4f6f8; text-align: center; padding: 15px; font-size: 12px; color: #888888;">
                &copy; 2025 ChildGrowth Insights. All rights reserved.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
    mail.send(msg)

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            token = serializer.dumps(email, salt="password-reset-salt")
            send_reset_email(email, token)
        flash("If email exists, a reset link has been sent.", "info")
        return redirect(url_for("login"))
    return render_template("forgot.html")


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(
            token, salt="password-reset-salt", max_age=3600
        )
    except Exception:
        flash("The reset link is invalid or expired.", "danger")
        return redirect(url_for("forgot"))

    if request.method == "POST":
        new_password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")

        if new_password != confirm_password:
            flash(
                "New password and confirmation do not match.", "danger"
            )
            return redirect(url_for("reset_password", token=token))

        if not is_strong_password(new_password):
            flash(
                "Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, and one symbol.",

                "warning"
            )
            return redirect(url_for("reset_password", token=token))

        hashed = bcrypt.generate_password_hash(new_password).decode("utf-8")
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = %s WHERE email = %s",
            (hashed, email),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Your password has been updated. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("reset.html")


# -------------------------------------------------
# DASHBOARD & CHILD SELECTION
# -------------------------------------------------
@app.route("/select-child", methods=["GET", "POST"])
@login_required
def select_child():
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM children WHERE parent_id=%s", (current_user.id,)
    )
    children = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == "POST":
        child_id = request.form.get("child_id")
        if child_id:
            session["selected_child"] = child_id
            return redirect(url_for("dashboard"))
        flash("Please choose a child.", "warning")

    return render_template("select_child.html", children=children)


@app.route("/dashboard")
@login_required
def dashboard():
    if "selected_child" not in session:
        return redirect(url_for("select_child"))

    child_id = session["selected_child"]

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    selected_child = cursor.fetchone()
    if not selected_child:
        flash("Child not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("select_child"))

    cursor.execute(
        "SELECT * FROM academic_scores WHERE child_id=%s ORDER BY date ASC",
        (child_id,),
    )
    scores = cursor.fetchall()
    subjects = sorted({row["subject"] for row in scores})
    for row in scores:
        if isinstance(row["date"], (datetime, date)):
            row["date_str"] = row["date"].strftime("%Y-%m")
        else:
            row["date_str"] = str(row["date"])[:7]

    cursor.execute(
        """
        SELECT module, result, updated_at
        FROM ai_results
        WHERE child_id=%s
          AND module IN ('preschool', 'learning', 'tutoring')
        """,
        (child_id,),
    )
    ai_results = cursor.fetchall()
    ai_map = {r["module"]: r for r in ai_results}

    preschool_ai = ai_map.get("preschool", {}).get(
        "result", "<p class='text-muted'>No preschool analysis yet.</p>"
    )
    learning_ai = ai_map.get("learning", {}).get(
        "result", "<p class='text-muted'>No learning style analysis yet.</p>"
    )
    tutoring_ai = ai_map.get("tutoring", {}).get(
        "result", "<p class='text-muted'>No tutoring recommendations yet.</p>"
    )

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_dashboard.html",
        selected_child=selected_child,
        scores=scores,
        subjects=subjects,
        preschool=[preschool_ai],
        learning=[learning_ai],
        tutoring=[tutoring_ai],
        active="dashboard",
    )


# -------------------------------------------------
# CHILDREN (standalone page)
# -------------------------------------------------
@app.route("/children", methods=["GET", "POST"])
@login_required
def children():
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        dob = request.form["dob"]
        age = request.form["age"]
        grade_level = request.form["grade_level"]
        gender = request.form["gender"]
        notes = request.form.get("notes", "")

        # Validate name contains only alphabet letters
        if not is_valid_name(name):
            flash("Child name must contain only alphabet letters and spaces.", "danger")
            cursor.execute(
                "SELECT * FROM children WHERE parent_id=%s", (current_user.id,)
            )
            children_list = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template("select_child.html", children=children_list)

        cursor.execute(
            """
            INSERT INTO children
            (parent_id, name, dob, age, grade_level, gender, notes)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (current_user.id, name, dob, age, grade_level, gender, notes),
        )
        conn.commit()
        flash("Child profile added!", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("children"))

    cursor.execute(
        "SELECT * FROM children WHERE parent_id=%s", (current_user.id,)
    )
    children_rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("children.html", children=children_rows)


# -------------------------------------------------
# PROFILE (no test management here anymore)
# -------------------------------------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (current_user.id,))
    user = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM children WHERE parent_id=%s", (current_user.id,)
    )
    children = cursor.fetchall()

    cursor.close()
    conn.close()

    # tests removed from profile in Option A – just pass empty list
    return render_template(
        "profile.html", user=user, children=children, tests=[]
    )

@app.route("/profile/edit", methods=["POST"])
@login_required
def edit_profile():
    name = request.form["name"].strip()
    email = request.form["email"].strip().lower()

    # Validate name contains only alphabet letters
    if not is_valid_name(name):
        flash("Name must contain only alphabet letters and spaces.", "danger")
        return redirect(url_for("profile"))  

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, current_user.id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile"))


@app.route("/profile/child/add", methods=["POST"])
@login_required
def add_child():
    name = request.form["name"]
    dob = request.form["dob"]
    age = request.form["age"]
    grade_level = request.form["grade_level"]
    gender = request.form["gender"]
    notes = request.form.get("notes", "")

    # Validate name contains only alphabet letters
    if not is_valid_name(name):
        flash("Child name must contain only alphabet letters and spaces.", "danger")
        return redirect(url_for("profile"))

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO children
        (parent_id, name, dob, age, grade_level, gender, notes)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (current_user.id, name, dob, age, grade_level, gender, notes),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Child profile added!", "success")
    return redirect(url_for("profile"))


@app.route("/profile/child/delete/<int:child_id>", methods=["POST"])
@login_required
def delete_child(child_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Child profile deleted.", "info")
    return redirect(url_for("profile"))


@app.route("/profile/child/edit/<int:child_id>", methods=["POST"])
@login_required
def edit_child(child_id):
    name = request.form["name"]
    dob = request.form["dob"]
    age = request.form["age"]
    grade_level = request.form["grade_level"]
    gender = request.form["gender"]
    notes = request.form.get("notes", "")

    # Validate name contains only alphabet letters
    if not is_valid_name(name):
        flash("Child name must contain only alphabet letters and spaces.", "danger")
        return redirect(url_for("profile"))

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE children
        SET name=%s, dob=%s, age=%s, grade_level=%s, gender=%s, notes=%s
        WHERE id=%s AND parent_id=%s
        """,
        (
            name,
            dob,
            age,
            grade_level,
            gender,
            notes,
            child_id,
            current_user.id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Child profile updated!", "success")
    return redirect(url_for("profile"))


# -------------------------------------------------
# ACADEMIC
# -------------------------------------------------
@app.route("/academic", methods=["GET", "POST"])
@login_required
def academic_progress():
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        subject = request.form.get("subject")
        if subject == "Other":
            subject = request.form.get("other_subject")

        score = request.form.get("score", type=int)
        year = request.form.get("year", type=int)
        month = request.form.get("month", type=int)

        if subject and score is not None and year and month:
            record_date = date(year, month, 1)
            cursor.execute(
                """
                INSERT INTO academic_scores (child_id, subject, score, date)
                VALUES (%s, %s, %s, %s)
                """,
                (child_id, subject, score, record_date),
            )
            conn.commit()
            flash("Academic record added successfully!", "success")
        else:
            flash("Please fill in all fields.", "danger")

        cursor.close()
        conn.close()
        return redirect(url_for("academic_progress"))

    cursor.execute(
        "SELECT * FROM academic_scores WHERE child_id = %s ORDER BY date ASC",
        (child_id,),
    )
    scores = cursor.fetchall()
    for row in scores:
        row["date_str"] = row["date"].strftime("%Y-%m")

    subjects = list({row["subject"] for row in scores})

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_academic.html",
        selected_child={"id": child_id},
        scores=scores,
        subjects=subjects,
        active="academic",
    )


@app.route("/academic/delete/<int:id>", methods=["POST"])
@login_required
def delete_academic(id):
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("academic_progress"))

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM academic_scores WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Academic record deleted successfully.", "success")
    return redirect(url_for("academic_progress"))


# -------------------------------------------------
# PRESCHOOL
# -------------------------------------------------
def calculate_months_difference(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (
        end_date.month - start_date.month
    )


@app.route("/dashboard/preschool", methods=["GET", "POST"])
@login_required
def preschool_tracker():
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("dashboard"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM children WHERE id=%s", (child_id,))
    child = cursor.fetchone()
    if not child:
        flash("Child not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))

    child_info = (
        f"Name: {child['name']}, Gender: {child['gender']}, "
        f"Date of Birth: {child['dob']}, Grade Level: {child['grade_level']}"
    )

    if request.method == "POST" and "domain" in request.form:
        domain = request.form["domain"]
        description = request.form["description"]
        form_date = request.form["date"]
        formatted_date = f"{form_date}-01"

        cursor.execute(
            """
            INSERT INTO preschool_assessments (child_id, domain, description, date)
            VALUES (%s, %s, %s, %s)
            """,
            (child_id, domain, description, formatted_date),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("preschool_tracker"))

    cursor.execute(
        "SELECT * FROM preschool_assessments WHERE child_id=%s ORDER BY date DESC",
        (child_id,),
    )
    assessments = cursor.fetchall()

    dob = child.get("dob")
    if isinstance(dob, (datetime, date)):
        dob_dt = datetime.combine(dob, datetime.min.time())
    elif isinstance(dob, str):
        dob_dt = datetime.strptime(dob, "%Y-%m-%d")
    else:
        dob_dt = None

    for a in assessments:
        milestone_date = a.get("date")
        if isinstance(milestone_date, (datetime, date)):
            milestone_dt = datetime.combine(
                milestone_date, datetime.min.time()
            )
            a["date_str"] = milestone_dt.strftime("%Y-%m")
        elif isinstance(milestone_date, str):
            a["date_str"] = milestone_date[:7]
            milestone_dt = datetime.strptime(a["date_str"], "%Y-%m")
        else:
            milestone_dt = None
            a["date_str"] = "Unknown"

        a["age_months"] = (
            calculate_months_difference(dob_dt, milestone_dt)
            if dob_dt and milestone_dt
            else None
        )

    cursor.execute(
        "SELECT * FROM ai_results WHERE child_id=%s AND module='preschool' LIMIT 1",
        (child_id,),
    )
    ai_row = cursor.fetchone()

    data_payload = json.dumps(assessments, default=str)
    benchmark_summary = None
    last_generated = None
    use_cached = False

    if not assessments:
        benchmark_summary = (
            "<p class='text-muted'>No preschool milestone data available yet. "
            "Add some assessments to view AI analysis.</p>"
        )
    else:
        if ai_row and ai_row.get("data") == data_payload:
            benchmark_summary = ai_row["result"]
            last_generated = ai_row["updated_at"] or ai_row["created_at"]
            use_cached = True
        else:
            try:
                combined_text = "\n".join(
                    f"- {a['domain']}: {a['description']} (at {a['age_months']} months)"
                    for a in assessments
                )

                prompt = f"""
                You are an early childhood development expert.

                This is the data of the child: {child_info}

                The following are recorded preschool milestones for a child, including their age in months when achieved:
                {combined_text}

                Based on these milestones, compare the child's development to standard age-based benchmarks in {benchmark_df.shape[0]} developmental records (see attached data sample below).

                {benchmark_df.to_string(index=False)}

                Summarize in clear, short language:
                - Areas that are age-appropriate
                - Areas that are delayed
                - Areas that are advanced for the child's age

                Follow the below rules strictly:
                - End with a one-sentence summary of overall development progress.
                - Provide the summary in HTML styled.
                - Do not self introduce yourself.
                """

                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                benchmark_summary = response.text.strip()

                if ai_row:
                    cursor.execute(
                        """
                        UPDATE ai_results
                        SET data=%s, result=%s, updated_at=NOW()
                        WHERE id=%s
                        """,
                        (data_payload, benchmark_summary, ai_row["id"]),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ai_results
                        (child_id, module, data, result, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, NOW(), NOW())
                        """,
                        (
                            child_id,
                            "preschool",
                            data_payload,
                            benchmark_summary,
                        ),
                    )
                conn.commit()

            except Exception as e:
                if "quota" in str(e).lower() or "api key" in str(e).lower():
                    cursor.close()
                    conn.close()
                    return jsonify({"error": "token_limit"})
                benchmark_summary = (
                    f"<p class='text-danger'>(Error generating analysis: {e})</p>"
                )

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_preschool.html",
        selected_child=child,
        assessments=assessments,
        benchmark_summary=benchmark_summary,
        last_generated=last_generated,
        use_cached=use_cached,
        active="preschool",
    )


@app.route("/preschool/delete/<int:id>", methods=["POST"])
@login_required
def delete_preschool(id):
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("dashboard"))

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM preschool_assessments WHERE id = %s", (id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Preschool record deleted.", "success")
    return redirect(url_for("preschool_tracker"))


# -------------------------------------------------
# LEARNING STYLE
# -------------------------------------------------
@app.route("/dashboard/learning", methods=["GET", "POST"])
@login_required
def learning_style():
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()
    if not child:
        cursor.close()
        conn.close()
        flash("Child not found.", "danger")
        return redirect(url_for("profile"))

    if request.method == "POST" and "observation" in request.form:
        observation = request.form["observation"]
        cursor.execute(
            """
            INSERT INTO learning_observations (child_id, observation, created_at)
            VALUES (%s, %s, NOW())
            """,
            (child_id, observation),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("learning_style"))

    # IMPORTANT: Option A — only admin-created tests (user_id IS NULL)
    cursor.execute(
    "SELECT * FROM tests ORDER BY id DESC"
    )
    user_tests = cursor.fetchall()

    cursor.execute(
        """
        SELECT * FROM learning_observations
        WHERE child_id=%s
        ORDER BY created_at DESC
        """,
        (child_id,),
    )
    learning_notes = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            ta.id AS answer_id,
            ta.test_id,
            ta.question_id,
            ta.answer,
            ta.created_at,
            t.name AS test_name,
            tq.question AS question_text
        FROM test_answers ta
        JOIN tests t ON ta.test_id = t.id
        JOIN test_questions tq ON ta.question_id = tq.id
        WHERE ta.child_id = %s
        ORDER BY ta.created_at DESC
        """,
        (child_id,),
    )
    test_answers = cursor.fetchall()

    combined_data = {"observations": learning_notes, "answers": test_answers}
    data_payload = json.dumps(
        combined_data, default=str, ensure_ascii=False, indent=2
    )

    cursor.execute(
        """
        SELECT * FROM ai_results
        WHERE child_id=%s AND module='learning'
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (child_id,),
    )
    cached = cursor.fetchone()

    use_cached = cached and cached["data"] == data_payload
    benchmark_summary = cached["result"] if use_cached else None
    last_generated = cached["updated_at"] if cached else None
    regen = request.args.get("regen")

    if (regen == "1" or not use_cached) and (learning_notes or test_answers):
        try:
            obs_text = (
                "\n".join(f"- {o['observation']}" for o in learning_notes)
                if learning_notes
                else "No observations."
            )

            test_grouped = {}
            for ans in test_answers:
                test_grouped.setdefault(ans["test_name"], []).append(ans)

            ans_text = ""
            for test_name, answers in test_grouped.items():
                ans_text += f"\n{test_name}:\n"
                for a in answers:
                    answer_val = a.get("answer")
                    question_text = a.get("question_text", "Unknown question")
                    if str(answer_val).isdigit():
                        ans_text += (
                            f"  - Q: {question_text}\n"
                            f"    A: {answer_val} (on scale 1–5)\n"
                        )
                    else:
                        ans_text += (
                            f"  - Q: {question_text}\n    A: {answer_val}\n"
                        )

            prompt = f"""
            You are an educational psychologist specializing in early childhood learning styles.

            Below are real observations and test responses for a preschool child.

            Observations:
            {obs_text}

            Test Answers:
            {ans_text}

            Based on this data, identify the child's most likely learning style (Visual, Auditory,
            Reading/Writing, Kinesthetic, or Mixed).
            Then write a short paragraph (3–5 sentences) explaining your reasoning.
            Finally, list 3–5 actionable suggestions for parent to support this learning style effectively.
            Keep the tone positive and easy to understand.
            Follow the below rules strictly:
            - Provide the summary in HTML stlyed.
            - Do not self introduced yourself.
            """

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            benchmark_summary = response.text.strip()

            if cached:
                cursor.execute(
                    """
                    UPDATE ai_results
                    SET data=%s, result=%s, updated_at=NOW()
                    WHERE id=%s
                    """,
                    (data_payload, benchmark_summary, cached["id"]),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO ai_results
                    (child_id, module, data, result, created_at, updated_at)
                    VALUES (%s, 'learning', %s, %s, NOW(), NOW())
                    """,
                    (child_id, data_payload, benchmark_summary),
                )
            conn.commit()
            last_generated = datetime.now()

        except Exception as e:
            if "token" in str(e).lower():
                cursor.close()
                conn.close()
                return jsonify({"error": "token_limit"})
            benchmark_summary = (
                f"<p class='text-danger'>(Error generating analysis: {e})</p>"
            )

    elif not learning_notes and not test_answers:
        benchmark_summary = (
            "<p class='text-muted'>No data available yet. "
            "Add observations or test answers first.</p>"
        )

    cursor.close()
    conn.close()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {
                "benchmark_summary": benchmark_summary,
                "last_generated": last_generated.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if last_generated
                else None,
                "use_cached": use_cached,
            }
        )

    return render_template(
        "dashboard.html",
        content_template="dashboard/_learning.html",
        selected_child=child,
        learning_notes=learning_notes,
        test_answers=test_answers,
        user_tests=user_tests,
        benchmark_summary=benchmark_summary,
        last_generated=last_generated,
        use_cached=use_cached,
        active="learning",
    )


# ---- Change password ----
@app.route("/profile/change-password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not all([current_password, new_password, confirm_password]):
        flash("Please fill in all password fields.", "warning")
        return redirect(url_for("profile"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT password FROM users WHERE id=%s", (current_user.id,)
    )
    user = cursor.fetchone()

    if not user or not bcrypt.check_password_hash(
        user["password"], current_password
    ):
        cursor.close()
        conn.close()
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("profile"))

    if new_password != confirm_password:
        cursor.close()
        conn.close()
        flash("New passwords do not match.", "danger")
        return redirect(url_for("profile"))

    if not is_strong_password(new_password):
        cursor.close()
        conn.close()
        flash(
            "Password must be at least 8 characters with uppercase, "
            "lowercase, and a special character.",
            "warning",
        )
        return redirect(url_for("profile"))

    hashed_password = bcrypt.generate_password_hash(new_password).decode(
        "utf-8"
    )
    cursor.execute(
        "UPDATE users SET password=%s WHERE id=%s",
        (hashed_password, current_user.id),
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Password changed successfully.", "success")
    return redirect(url_for("profile"))


# ---- AJAX: get questions for a test (admin-created only) ----
@app.route("/learning/test_questions/<int:test_id>")
@login_required
def get_test_questions(test_id):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # Just ensure the test exists
    cursor.execute("SELECT * FROM tests WHERE id=%s", (test_id,))
    test = cursor.fetchone()
    if not test:
        cursor.close()
        conn.close()
        return jsonify([])

    cursor.execute("SELECT * FROM test_questions WHERE test_id=%s", (test_id,))
    questions = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(questions)



@app.route("/learning/take_test/<int:child_id>", methods=["POST"])
@login_required
def take_learning_test(child_id):
    conn = get_db_conn()
    cursor = conn.cursor()

    test_id = request.form.get("test_id")
    if not test_id:
        flash("Please select a test.", "danger")
        return redirect(url_for("learning_style"))

    for key in request.form:
        if key.startswith("answers[") and key.endswith("[answer]"):
            idx = key.split("[")[1].split("]")[0]
            question_id = request.form.get(f"answers[{idx}][question_id]")
            answer_value = request.form.get(f"answers[{idx}][answer]")
            if question_id and answer_value is not None:
                cursor.execute(
                    """
                    INSERT INTO test_answers
                    (child_id, test_id, question_id, answer, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                    """,
                    (child_id, test_id, question_id, answer_value),
                )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Test answers submitted successfully.", "success")
    return redirect(url_for("learning_style"))


@app.route("/learning/observation/submit/<int:child_id>", methods=["POST"])
@login_required
def submit_learning_observation(child_id):
    observation = request.form.get("observation")
    if not observation:
        flash("Observation cannot be empty.", "danger")
        return redirect(url_for("learning_style"))

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO learning_observations (child_id, observation, created_at)
        VALUES (%s, %s, NOW())
        """,
        (child_id, observation),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("learning_style"))


@app.route("/learning/observation/delete/<int:observation_id>", methods=["POST"])
@login_required
def delete_learning_observation(observation_id):
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE lo FROM learning_observations lo
        JOIN children c ON c.id = lo.child_id
        WHERE lo.id=%s AND c.parent_id=%s
        """,
        (observation_id, current_user.id),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(request.referrer or url_for("profile"))


# -------------------------------------------------
# TUTORING, INSIGHTS, PLAN, RESOURCES
# (unchanged logic, just using get_db_conn)
# -------------------------------------------------
#  👉 I’ll keep the rest of these four modules identical
#     to your previous working version, just cleaned
#     to use get_db_conn and with @login_required.
#     (They are long, but logic is the same.)

# --- TUTORING ---
@app.route("/dashboard/tutoring")
@login_required
def tutoring_recommendations():
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()
    if not child:
        flash("Child not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))

    cursor.execute(
        """
        SELECT module, result, updated_at
        FROM ai_results
        WHERE child_id=%s AND module IN ('learning', 'preschool')
        """,
        (child_id,),
    )
    child_ai = cursor.fetchall()

    learning_result = next(
        (r["result"] for r in child_ai if r["module"] == "learning"),
        None,
    )
    preschool_result = next(
        (r["result"] for r in child_ai if r["module"] == "preschool"),
        None,
    )

    cursor.execute(
        "SELECT * FROM ai_results WHERE child_id=%s AND module='tutoring' LIMIT 1",
        (child_id,),
    )
    cached = cursor.fetchone()

    regen = request.args.get("regen")

    data_payload = json.dumps(
        {"learning": learning_result, "preschool": preschool_result},
        ensure_ascii=False,
        indent=2,
    )
    use_cached = cached and cached["data"] == data_payload and not regen
    tutoring_summary = cached["result"] if use_cached else None
    last_generated = cached["updated_at"] if cached else None

    if not learning_result and not preschool_result:
        tutoring_summary = (
            "<p class='text-muted'>No AI analysis data available yet. "
            "Run preschool and learning style assessments first.</p>"
        )
    elif regen == "1" or not use_cached:
        try:
            prompt = f"""
            You are an expert child education advisor.

            You will analyze a preschool child's development and learning style to recommend tutoring or support areas.

            --- Preschool Development Summary ---
            {preschool_result if preschool_result else "No preschool data available."}

            --- Learning Style Analysis ---
            {learning_result if learning_result else "No learning style data available."}

            Based on the above, identify:
            1. The child’s potential weak areas or skills that may need support.
            2. Subjects or developmental domains where tutoring or extra help would be most beneficial.
            3. Personalized activity or tutoring style recommendations aligned with the learning style.

            Output clear, structured suggestions in HTML format:
            - Use <ul><li> for lists.
            - End with a short summary paragraph for parents.
            - Avoid self-reference or disclaimers.
            """

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            tutoring_summary = response.text.strip()

            if cached:
                cursor.execute(
                    """
                    UPDATE ai_results
                    SET data=%s, result=%s, updated_at=NOW()
                    WHERE id=%s
                    """,
                    (data_payload, tutoring_summary, cached["id"]),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO ai_results
                    (child_id, module, data, result, created_at, updated_at)
                    VALUES (%s, 'tutoring', %s, %s, NOW(), NOW())
                    """,
                    (child_id, data_payload, tutoring_summary),
                )
            conn.commit()
            last_generated = datetime.now()

        except Exception as e:
            if "token" in str(e).lower():
                cursor.close()
                conn.close()
                return jsonify({"error": "token_limit"})
            tutoring_summary = (
                f"<p class='text-danger'>(Error generating recommendations: {e})</p>"
            )

    cursor.close()
    conn.close()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {
                "tutoring_summary": tutoring_summary,
                "last_generated": last_generated.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if last_generated
                else None,
                "use_cached": use_cached,
            }
        )

    return render_template(
        "dashboard.html",
        content_template="dashboard/_tutoring.html",
        selected_child=child,
        tutoring_summary=tutoring_summary,
        last_generated=last_generated,
        use_cached=use_cached,
        active="tutoring",
    )


# --- AI INSIGHTS ---
@app.route("/dashboard/insights")
@login_required
def ai_insights():
    child_id = session.get("selected_child")
    if not child_id:
        flash("Please select a child first.", "warning")
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()
    if not child:
        cursor.close()
        conn.close()
        flash("Child not found.", "danger")
        return redirect(url_for("dashboard"))

    cursor.execute(
        """
        SELECT subject, score, date
        FROM academic_scores
        WHERE child_id=%s
        ORDER BY date ASC
        """,
        (child_id,),
    )
    scores = cursor.fetchall()

    strengths = []
    weaknesses = []
    for row in scores:
        subject = row["subject"]
        score = row["score"]
        if score is None:
            continue
        if score >= 80:
            strengths.append(f"{subject} is a strong subject (score {score}).")
        elif score <= 50:
            weaknesses.append(f"{subject} needs improvement (score {score}).")

    payload_obj = {"scores": scores}
    data_payload = json.dumps(payload_obj, default=str, ensure_ascii=False)

    cursor.execute(
        "SELECT * FROM ai_results WHERE child_id=%s AND module='insights' LIMIT 1",
        (child_id,),
    )
    cached = cursor.fetchone()

    regen = request.args.get("regen")
    use_cached = cached and cached["data"] == data_payload and not regen

    ai_summary = None
    last_generated = cached["updated_at"] if cached else None

    if use_cached:
        ai_summary = cached["result"]
    else:
        if scores:
            try:
                score_lines = [
                    f"{row['subject']}: {row['score']}"
                    for row in scores
                    if row["score"] is not None
                ]
                scores_text = "\n".join(score_lines)

                prompt = f"""
You are an educational psychologist for preschool children.

Child name: {child['name']}
Age: {child.get('age', 'unknown')}

Here are this child's recent subjects and scores:
{scores_text}

Based on these scores, write a short, parent-friendly summary in 3–5 sentences.
Explain:
- Key strengths
- Areas that may need more support
- 1–2 gentle, practical suggestions for what parents can do at home.

Use warm, encouraging language.
Do NOT mention exact score numbers or percentages; just describe performance levels
(e.g., "very strong in math", "needs a little extra help in reading").
"""

                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                ai_summary = response.text.strip()

                if cached:
                    cursor.execute(
                        """
                        UPDATE ai_results
                        SET data=%s, result=%s, updated_at=NOW()
                        WHERE id=%s
                        """,
                        (data_payload, ai_summary, cached["id"]),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ai_results
                        (child_id, module, data, result, created_at, updated_at)
                        VALUES (%s, 'insights', %s, %s, NOW(), NOW())
                        """,
                        (child_id, data_payload, ai_summary),
                    )
                conn.commit()
                last_generated = datetime.now()
            except Exception as e:
                app.logger.error(f"AI insights error: {e}")
                ai_summary = None
        else:
            ai_summary = None

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_insights.html",
        selected_child=child,
        scores=scores,
        strengths=strengths,
        weaknesses=weaknesses,
        ai_summary=ai_summary,
        last_generated=last_generated,
        active="insights",
    )


# --- LEARNING PLAN ---
@app.route("/dashboard/plan")
@login_required
def learning_plan():
    child_id = session.get("selected_child")
    if not child_id:
        flash("Please select a child first.", "warning")
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()
    if not child:
        cursor.close()
        conn.close()
        flash("Child not found.", "danger")
        return redirect(url_for("dashboard"))

    cursor.execute(
        """
        SELECT subject, score, date
        FROM academic_scores
        WHERE child_id=%s
        ORDER BY date ASC
        """,
        (child_id,),
    )
    scores = cursor.fetchall()

    score_lines = [
        f"{row['subject']}: {row['score']}"
        for row in scores
        if row["score"] is not None
    ]
    scores_text = "\n".join(score_lines) if score_lines else "No academic scores yet."

    cursor.execute(
        """
        SELECT module, result
        FROM ai_results
        WHERE child_id=%s AND module IN ('learning', 'preschool', 'tutoring')
        """,
        (child_id,),
    )
    other_ai = cursor.fetchall()

    learning_result = next(
        (r["result"] for r in other_ai if r["module"] == "learning"), None
    )
    preschool_result = next(
        (r["result"] for r in other_ai if r["module"] == "preschool"), None
    )
    tutoring_result = next(
        (r["result"] for r in other_ai if r["module"] == "tutoring"), None
    )

    payload_obj = {
        "scores": scores,
        "learning_result": learning_result,
        "preschool_result": preschool_result,
        "tutoring_result": tutoring_result,
    }
    data_payload = json.dumps(payload_obj, default=str, ensure_ascii=False)

    cursor.execute(
        "SELECT * FROM ai_results WHERE child_id=%s AND module='learning_plan' LIMIT 1",
        (child_id,),
    )
    cached = cursor.fetchone()

    regen = request.args.get("regen")
    use_cached = cached and cached["data"] == data_payload and not regen

    plan_html = None
    last_generated = cached["updated_at"] if cached else None

    if use_cached:
        plan_html = cached["result"]
    else:
        if scores or learning_result or preschool_result or tutoring_result:
            try:
                child_info = (
                    f"Name: {child['name']}, Age: {child.get('age', 'unknown')}, "
                    f"Grade Level: {child.get('grade_level', 'unknown')}"
                )

                prompt = f"""
You are an expert preschool educational planner.

Child information:
{child_info}

Academic scores:
{scores_text}

Learning style analysis (if available):
{learning_result or "Not available."}

Preschool development summary (if available):
{preschool_result or "Not available."}

Tutoring recommendations (if available):
{tutoring_result or "Not available."}

Your task:
Create a one-week personalized learning plan for this child.

OUTPUT REQUIREMENTS (VERY IMPORTANT):
- Return HTML ONLY (no Markdown, no explanations outside HTML).
- Use this exact structure:

<h3>Learning Plan Summary</h3>
<p>Write 3–6 warm, parent-friendly sentences describing:
- What the child is doing well
- What to focus on this week
- Overall encouragement for the family.
Do NOT mention exact scores or percentages.</p>

<h3>Weekly Action Plan</h3>
<table class="table table-striped">
  <thead>
    <tr><th>Day</th><th>Recommended Activities</th></tr>
  </thead>
  <tbody>
  </tbody>
</table>

<h3>Long-Term Strategy</h3>
<ul>
  <li>3–5 bullet points about habits, routines, and ways parents can support the child over the next few months.</li>
</ul>

RULES:
- Make activities short (around 10–20 minutes each) and realistic for a preschool child.
- Align activities with the child's likely learning style if that information is available.
- Use simple, encouraging language that Malaysian parents can easily understand.
- Do NOT mention exam scores, percentages, or grade labels directly.
"""

                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                plan_html = response.text.strip()

                if cached:
                    cursor.execute(
                        """
                        UPDATE ai_results
                        SET data=%s, result=%s, updated_at=NOW()
                        WHERE id=%s
                        """,
                        (data_payload, plan_html, cached["id"]),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ai_results
                        (child_id, module, data, result, created_at, updated_at)
                        VALUES (%s, 'learning_plan', %s, %s, NOW(), NOW())
                        """,
                        (child_id, data_payload, plan_html),
                    )
                conn.commit()
                last_generated = datetime.now()

            except Exception as e:
                app.logger.error(f"Learning plan AI error: {e}")
                plan_html = (
                    "<p class='text-danger'>(Error generating learning plan. "
                    "Please try again later.)</p>"
                )
        else:
            plan_html = (
                "<p class='text-muted'>Not enough data yet. "
                "Please add some academic scores and/or run other AI analyses first.</p>"
            )

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_plan.html",
        selected_child=child,
        plan_html=plan_html,
        last_generated=last_generated,
        use_cached=use_cached,
        active="learning_plan",
    )


# --- RESOURCES HUB ---
@app.route("/dashboard/resources")
@login_required
def resources_hub():
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()
    if not child:
        cursor.close()
        conn.close()
        flash("Child not found.", "danger")
        return redirect(url_for("dashboard"))

    cursor.execute(
        """
        SELECT subject, score, date
        FROM academic_scores
        WHERE child_id=%s
        ORDER BY date DESC
        """,
        (child_id,),
    )
    scores = cursor.fetchall()

    cursor.execute(
        """
        SELECT result
        FROM ai_results
        WHERE child_id=%s AND module='learning'
        ORDER BY updated_at DESC
        LIMIT 1
        """,
        (child_id,),
    )
    learning_row = cursor.fetchone()
    learning_summary = learning_row["result"] if learning_row else None

    context_data = {
        "scores": scores,
        "learning_summary": learning_summary,
        "age": child.get("age"),
        "grade_level": child.get("grade_level"),
    }
    data_payload = json.dumps(context_data, default=str, ensure_ascii=False)

    regen = request.args.get("regen")

    cursor.execute(
        """
        SELECT *
        FROM ai_results
        WHERE child_id=%s AND module='resources'
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (child_id,),
    )
    cached = cursor.fetchone()

    use_cached = cached and cached["data"] == data_payload and not regen
    resources_html = cached["result"] if use_cached else None
    last_generated = cached["updated_at"] if cached else None

    if not use_cached:
        if not scores and not learning_summary:
            resources_html = """
            <p class='text-muted'>
                No learning data available yet. Please add some academic scores
                or run the Learning Style Analyzer first.
            </p>
            """
        else:
            score_lines = [
                f"{row['subject']}: {row['score']}"
                for row in scores
                if row.get("score") is not None
            ]
            scores_text = (
                "\n".join(score_lines) if score_lines else "No formal scores."
            )

            prompt = f"""
You are an educational content specialist for preschool children.

Child profile:
- Name: {child['name']}
- Age: {child.get('age', 'unknown')}
- Grade level: {child.get('grade_level', 'Preschool')}

Academic overview (subject: score):
{scores_text}

Learning style summary (may be HTML):
{learning_summary if learning_summary else "No learning style data available."}

Based on this information, create a curated Educational Resources Hub
for this child.

Output in HTML with these sections:

<h3>Suggested Resources Overview</h3>
<p>Write a 3–5 sentence, parent-friendly summary of what types of resources
   will help this child, focusing on both strengths and areas needing support.</p>

<h3>Videos</h3>
<ul>
  <li><strong>Title</strong> – short description (target skill, approximate duration, what parents should do while watching)</li>
</ul>

<h3>Games & Apps</h3>
<ul>
  <li><strong>Title</strong> – short description (type: digital game / mobile app / offline game, target subject or skill)</li>
</ul>

<h3>Books & Reading Materials</h3>
<ul>
  <li><strong>Title</strong> – short description (reading level, themes, how it supports their learning)</li>
</ul>

Rules:
- All resources must be suitable for a {child.get('age', 'preschool')}-year-old preschool child.
- Prioritize subjects or skills where the child is weaker, but still support their strengths.
- Do NOT include real URLs; just describe the type of video/game/app/book.
- Do NOT mention exact scores or percentages.
- Use warm, encouraging language for parents.
"""

            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                resources_html = response.text.strip()

                if cached:
                    cursor.execute(
                        """
                        UPDATE ai_results
                        SET data=%s, result=%s, updated_at=NOW()
                        WHERE id=%s
                        """,
                        (data_payload, resources_html, cached["id"]),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ai_results
                        (child_id, module, data, result, created_at, updated_at)
                        VALUES (%s, 'resources', %s, %s, NOW(), NOW())
                        """,
                        (child_id, data_payload, resources_html),
                    )
                conn.commit()
                last_generated = datetime.now()
            except Exception as e:
                app.logger.error(f"Resources hub AI error: {e}")
                if not resources_html:
                    resources_html = (
                        "<p class='text-danger'>Unable to generate resources at the moment.</p>"
                    )

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_resources.html",
        selected_child=child,
        resources_html=resources_html,
        last_generated=last_generated,
        use_cached=use_cached,
        active="resources",
    )


# -------------------------------------------------
# ADMIN AREA
# -------------------------------------------------
@app.route("/admin/dashboard")
@login_required
@roles_required("admin")
def admin_dashboard():
    return render_template("admin/dashboard.html", active="admin")


@app.route("/admin/users")
@login_required
@roles_required("admin")
def admin_users():
    search = request.args.get("q", "").strip()

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    if search:
        like = f"%{search}%"
        cursor.execute(
            """
            SELECT id, name, email, role, created_at
            FROM users
            WHERE name LIKE %s
               OR email LIKE %s
               OR CAST(id AS CHAR) LIKE %s
            ORDER BY created_at DESC
            """,
            (like, like, like),
        )
    else:
        cursor.execute(
            """
            SELECT id, name, email, role, created_at
            FROM users
            ORDER BY created_at DESC
            """
        )

    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin/users.html", users=users, search=search)


@app.route("/admin/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def admin_edit_user(user_id):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, email, role FROM users WHERE id=%s", (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        flash("User not found.", "danger")
        return redirect(url_for("admin_users"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email:
            flash("Name and email are required.", "warning")
            cursor.close()
            conn.close()
            return render_template("admin/edit_user.html", user=user)
            
        # Validate name contains only alphabet letters
        if not is_valid_name(name):
            flash("Name must contain only alphabet letters and spaces.", "danger")
            cursor.close()
            conn.close()
            return render_template("admin/edit_user.html", user=user)

        try:
            if password:
                hashed = bcrypt.generate_password_hash(password).decode(
                    "utf-8"
                )
                cursor.execute(
                    """
                    UPDATE users
                    SET name=%s, email=%s, password=%s
                    WHERE id=%s
                    """,
                    (name, email, hashed, user_id),
                )
            else:
                cursor.execute(
                    """
                    UPDATE users
                    SET name=%s, email=%s
                    WHERE id=%s
                    """,
                    (name, email, user_id),
                )

            conn.commit()
            flash("User updated successfully.", "success")

        except mysql.connector.errors.IntegrityError:
            conn.rollback()
            flash(
                "That email is already in use by another account.", "danger"
            )
            cursor.close()
            conn.close()
            return render_template("admin/edit_user.html", user=user)

        cursor.close()
        conn.close()
        return redirect(url_for("admin_users"))

    cursor.close()
    conn.close()
    return render_template("admin/edit_user.html", user=user)


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@login_required
@roles_required("admin")
def admin_delete_user(user_id):
    if user_id == current_user.id:
        flash(
            "You cannot delete your own account while logged in.", "warning"
        )
        return redirect(url_for("admin_users"))

    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM children WHERE parent_id = %s", (user_id,)
    )
    (child_count,) = cursor.fetchone()

    if child_count > 0:
        cursor.close()
        conn.close()
        flash(
            "This user still has child profiles linked. "
            "Delete or reassign them first.",
            "danger",
        )
        return redirect(url_for("admin_users"))

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("User account deleted successfully.", "success")
    return redirect(url_for("admin_users"))


# ---- ADMIN TEST MANAGEMENT (GLOBAL TESTS) ----
@app.route("/admin/tests")
@login_required
@roles_required("admin")
def admin_tests():
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT t.id, t.name, t.user_id, u.name AS owner_name
        FROM tests t
        LEFT JOIN users u ON t.user_id = u.id
        ORDER BY t.id DESC
        """
    )
    tests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin/test.html", tests=tests)


@app.route("/admin/tests/create", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def admin_create_test():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        questions = request.form.getlist("questions[]")
        categories = request.form.getlist("categories[]")
        media_files = request.files.getlist("question_media[]")

        conn = get_db_conn()
        cursor = conn.cursor()

        # 🔴 OLD: user_id = NULL  (causes error)
        # cursor.execute(
        #     "INSERT INTO tests (name, user_id) VALUES (%s, NULL)", (name,)
        # )

        # ✅ NEW: store the ID of the logged-in admin
        cursor.execute(
            "INSERT INTO tests (name, user_id) VALUES (%s, %s)",
            (name, current_user.id),
        )
        test_id = cursor.lastrowid

        for idx, (q, cat) in enumerate(zip(questions, categories)):
            file_obj = media_files[idx] if idx < len(media_files) else None
            media_type, media_path = save_question_media(file_obj, test_id, idx)

            cursor.execute(
                """
                INSERT INTO test_questions
                (test_id, question, answer_type, category, media_type, media_path)
                VALUES (%s, %s, 'scale', %s, %s, %s)
                """,
                (test_id, q, cat, media_type, media_path),
            )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Test created successfully!", "success")
        return redirect(url_for("admin_tests"))

    return render_template("admin/create_test.html")




@app.route("/admin/tests/<int:test_id>/edit", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def admin_edit_test(test_id):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tests WHERE id=%s", (test_id,))
    test = cursor.fetchone()

    cursor.execute("SELECT * FROM test_questions WHERE test_id=%s", (test_id,))
    questions = cursor.fetchall()

    if not test:
        cursor.close()
        conn.close()
        flash("Test not found.", "danger")
        return redirect(url_for("admin_tests"))

    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        new_questions = request.form.getlist("questions[]")
        new_categories = request.form.getlist("categories[]")
        media_files = request.files.getlist("question_media[]")

        # Safety: if categories shorter than questions, pad
        if len(new_categories) < len(new_questions):
            new_categories = (
                new_categories + ["reading"] * len(new_questions)
            )[: len(new_questions)]

        # Update test name
        cursor.execute(
            "UPDATE tests SET name=%s WHERE id=%s", (new_name, test_id)
        )

        # Remove old questions (and their media)
        cursor.execute("DELETE FROM test_questions WHERE test_id=%s", (test_id,))

        # Re-insert questions with media
        for idx, (q, cat) in enumerate(zip(new_questions, new_categories)):
            file_obj = media_files[idx] if idx < len(media_files) else None
            media_type, media_path = save_question_media(file_obj, test_id, idx)

            cursor.execute(
                """
                INSERT INTO test_questions
                (test_id, question, answer_type, category, media_type, media_path)
                VALUES (%s, %s, 'scale', %s, %s, %s)
                """,
                (test_id, q, cat, media_type, media_path),
            )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Test updated!", "success")
        return redirect(url_for("admin_tests"))

    cursor.close()
    conn.close()

    return render_template(
        "admin/edit_test.html", test=test, questions=questions
    )



@app.route("/admin/tests/<int:test_id>/delete", methods=["POST"])
@login_required
@roles_required("admin")
def admin_delete_test(test_id):
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM test_questions WHERE test_id=%s", (test_id,))
    cursor.execute("DELETE FROM tests WHERE id=%s", (test_id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Test deleted.", "success")
    return redirect(url_for("admin_tests"))


# -------------------------------------------------
# INDEX
# -------------------------------------------------
@app.route("/")
def index():
    if current_user.is_authenticated:
        # send admin to admin dashboard, parents to dashboard
        if normalize_role(current_user.role) == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
