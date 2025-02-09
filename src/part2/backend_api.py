import pandas as pd
import mysql.connector
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load the Excel file dynamically
file_path = "resources/poster_judge_full_matrix.xlsx"

# Database connection setup
def get_db_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="research"
    )

def get_judge_name(judge_id):
    """Fetch first and last name of the judge from the database using judge_number."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT first_name, last_name FROM judges WHERE judge_number = %s"
        cursor.execute(query, (judge_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return f"{result['first_name']} {result['last_name']}"
        return None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_poster_title(poster_number):
    """Fetch the title of a poster from the database using poster_number."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT title FROM abstracts WHERE poster_number = %s"
        cursor.execute(query, (poster_number,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result and result["title"]:
            return result["title"]
        return f"Poster {poster_number} (No Title Found)"
    except Exception as e:
        print(f"Database error: {e}")
        return f"Poster {poster_number} (Error Fetching Title)"

def load_excel():
    """Load the judges.xlsx file dynamically on each request."""
    try:
        judges_df = pd.read_excel(file_path, dtype=str)  # Read all as strings
        judges_df.columns = judges_df.columns.map(lambda x: str(x).strip())  # Normalize column names
        return judges_df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

@app.route("/")
def home():
    return render_template("login_page.html")  # Default page

@app.route("/login_page.html")
def login_page():
    return render_template("login_page.html")

@app.route("/dashboard.html")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    judge_id = str(data.get("judge_id")).strip()  # Convert judge ID to string

    judges_df = load_excel()
    if judges_df is None or judge_id not in judges_df.columns:
        return jsonify({"success": False, "message": f"Invalid Judge ID: {judge_id}"})

    return jsonify({"success": True, "judge_id": judge_id})

@app.route("/dashboard", methods=["GET"])
def get_assigned_posters():
    judge_id = str(request.args.get("judge_id")).strip()  # Convert to string

    judges_df = load_excel()
    if judges_df is None or judge_id not in judges_df.columns:
        return jsonify({"success": False, "message": f"Invalid Judge ID: {judge_id}"})

    # Fetch the judge's full name from the database
    judge_name = get_judge_name(judge_id)
    if not judge_name:
        judge_name = f"Judge {judge_id}"  # Fallback if no name is found

    # Retrieve assigned posters
    poster_column = "Poster Number"  # Correct column for poster IDs
    assigned_posters = judges_df[judges_df[judge_id].isin(["1", 1])][poster_column].tolist()

    # Fetch poster titles from the database
    posters_data = [{"id": poster, "title": get_poster_title(poster)} for poster in assigned_posters]

    return render_template("dashboard.html", judge_id=judge_id, judge_name=judge_name, posters=posters_data)

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.json
    judge_id = str(data.get("judge_id")).strip()  # Convert to string
    poster_id = data.get("poster_id")  # Poster Number from Excel
    score = data.get("score")

    # Validate required data
    if not judge_id or not poster_id or score is None:
        return jsonify({"success": False, "message": "Missing required data: judge_id, poster_id, and score are required."})

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the abstract_id using the poster_number
        cursor.execute("SELECT id FROM abstracts WHERE poster_number = %s", (poster_id,))
        abstract_result = cursor.fetchone()

        if not abstract_result:
            return jsonify({"success": False, "message": f"Poster {poster_id} not found in abstracts."})

        abstract_id = abstract_result["id"]  # Get the abstract UUID

        # Fetch the judge UUID using the judge_number
        cursor.execute("SELECT id FROM judges WHERE judge_number = %s", (judge_id,))
        judge_result = cursor.fetchone()

        if not judge_result:
            return jsonify({"success": False, "message": f"Judge {judge_id} not found in judges."})

        judge_uuid = judge_result["id"]  # Get the judge UUID

        # Check if a score already exists for this judge and abstract
        cursor.execute(
            "SELECT * FROM poster_score WHERE judge_id = %s AND abstract_id = %s",
            (judge_uuid, abstract_id),
        )
        existing_score = cursor.fetchone()

        if existing_score:
            # Update the existing score
            cursor.execute(
                "UPDATE poster_score SET score = %s WHERE judge_id = %s AND abstract_id = %s",
                (score, judge_uuid, abstract_id),
            )
            message = "Score updated successfully!"
        else:
            # Insert a new score
            cursor.execute(
                "INSERT INTO poster_score (judge_id, abstract_id, score) VALUES (%s, %s, %s)",
                (judge_uuid, abstract_id, score),
            )
            message = "Score submitted successfully!"

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": message})

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "An error occurred while submitting the score."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)