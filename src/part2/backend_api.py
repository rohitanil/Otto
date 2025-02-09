# import sys
# import os
# import mysql.connector
# from flask import Flask, request, jsonify, render_template

# # Dynamically add the 'src' directory to Python's module search path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# # Database Connection Function (Replacing db_connection.py)
# def get_cursor():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",  
#             user="user",  
#             password="password",  
#             database="research"  
#         )
#         cursor = conn.cursor()
#         return conn, cursor
#     except mysql.connector.Error as err:
#         print("Error:", err)
#         return None, None

# app = Flask(__name__, template_folder="templates", static_folder="static")

# @app.route("/")
# def home():
#     return render_template("login_page.html")  # Default page

# @app.route("/login_page.html")
# def login_page():
#     return render_template("login_page.html")

# @app.route("/dashboard.html")
# def dashboard_page():
#     return render_template("dashboard.html")

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     judge_id = data.get("judge_id")

#     conn, cursor = get_cursor()
#     if not conn:
#         return jsonify({"success": False, "message": "Database connection failed."})

#     try:
#         query = "SELECT id FROM judges WHERE id = %s;"
#         cursor.execute(query, (judge_id,))
#         result = cursor.fetchone()
        
#         cursor.close()
#         conn.close()
        
#         if result:
#             return jsonify({"success": True, "judge_id": result[0]})
#         else:
#             return jsonify({"success": False, "message": "Invalid Judge ID"})
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)})

# @app.route("/dashboard", methods=["GET"])
# def get_assigned_posters():
#     judge_id = request.args.get("judge_id")

#     conn, cursor = get_cursor()
#     if not conn:
#         return jsonify({"success": False, "message": "Database connection failed."})

#     try:
#         query = """
#         SELECT p.poster_number, a.title 
#         FROM judge_assignment AS p
#         JOIN abstracts AS a ON p.poster_number = a.poster_number
#         WHERE p.judge_id = %s;
#         """
#         cursor.execute(query, (judge_id,))
#         posters = cursor.fetchall()
        
#         cursor.close()
#         conn.close()
        
#         return jsonify({"success": True, "posters": [{"id": p[0], "title": p[1]} for p in posters]})
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)})

# @app.route("/submit_score", methods=["POST"])
# def submit_score():
#     data = request.json
#     judge_id = data.get("judge_id")
#     poster_id = data.get("poster_id")
#     score = data.get("score")

#     conn, cursor = get_cursor()
#     if not conn:
#         return jsonify({"success": False, "message": "Database connection failed."})

#     try:
#         query = """
#         INSERT INTO poster_score (judge1_id, abstract_id, score1) 
#         VALUES (%s, %s, %s)
#         ON DUPLICATE KEY UPDATE score1 = VALUES(score1);
#         """
#         cursor.execute(query, (judge_id, poster_id, score))
#         conn.commit()
        
#         cursor.close()
#         conn.close()
        
#         return jsonify({"success": True, "message": "Score submitted successfully!"})
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)

import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load the Excel file and ensure Judge IDs are strings
file_path = "judges.xlsx"
def load_excel():
    """ Load the judges.xlsx file dynamically on each request """
    try:
        judges_df = pd.read_excel(file_path, dtype=str)
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
    judge_id = str(data.get("judge_id"))  # Ensure judge ID is a string

    # Check if judge ID exists in Excel columns
    if judges_df is None or judge_id not in judges_df.columns:
        return jsonify({"success": False, "message": f"Invalid Judge ID: {judge_id}"})

    return jsonify({"success": True, "judge_id": judge_id})

@app.route("/dashboard", methods=["GET"])
def get_assigned_posters():
    judge_id = request.args.get("judge_id")

    judges_df = load_excel()
    if judges_df is None or judge_id not in judges_df.columns:
        return jsonify({"success": False, "message": f"Invalid Judge ID: {judge_id}"})

    # Find posters assigned to this judge (where value is '1')
    assigned_posters = judges_df[judges_df[judge_id] == "1"]["Poster_ID"].tolist()

    # Generate placeholder titles
    posters_data = [{"id": poster, "title": f"Poster {poster} Title"} for poster in assigned_posters]

    return render_template("dashboard.html", judge_id=judge_id, posters=posters_data)

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.json
    judge_id = str(data.get("judge_id"))
    poster_id = data.get("poster_id")
    score = data.get("score")

    # Validate required data
    if not judge_id or not poster_id or score is None:
        return jsonify({"success": False, "message": "Missing required data: judge_id, poster_id, and score are required."})

    # Simulate score storage (print for debugging, later save to Excel or DB)
    print(f"Judge {judge_id} submitted score {score} for Poster {poster_id}")

    return jsonify({"success": True, "message": "Score submitted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)