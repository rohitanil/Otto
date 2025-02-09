import db_connection as db
import pandas as pd
import os

def file1():
    conn, cursor = db.get_cursor()

    query = """
        SELECT 
            a.poster_number, a.title, a.abstract, 
            a.advisor_first_name, a.advisor_last_name, a.program,
            j1.judge_number AS judge_1, j2.judge_number AS judge_2
        FROM abstracts a
        LEFT JOIN poster_score ps1 ON a.id = ps1.abstract_id
        LEFT JOIN poster_score ps2 ON a.id = ps2.abstract_id AND ps1.judge_id < ps2.judge_id
        LEFT JOIN judges j1 ON ps1.judge_id = j1.id
        LEFT JOIN judges j2 ON ps2.judge_id = j2.id
        WHERE ps1.judge_id IS NOT NULL AND ps2.judge_id IS NOT NULL
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["Poster Number", "Title", "Abstract", "Advisor First Name", "Advisor Last Name", "Program", "Judge-1",
               "Judge-2"]
    df = pd.DataFrame(rows, columns=columns)
    df = df.sort_values(by="Poster Number", ascending=True)
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Creates the folder if it doesn't exist
    excel_filename = os.path.join(output_dir,"output/abstracts_with_judges.xlsx")
    df.to_excel(excel_filename, index=False)
    print(f"Excel file '{excel_filename}' generated successfully.")
    cursor.close()
    conn.close()


def file2():
    conn, cursor = db.get_cursor()

    query = """
        SELECT 
            j.judge_number, j.first_name, j.last_name, j.department, j.hour_available,
            MAX(CASE WHEN ps_row = 1 THEN a.poster_number END) AS poster_1,
            MAX(CASE WHEN ps_row = 2 THEN a.poster_number END) AS poster_2,
            MAX(CASE WHEN ps_row = 3 THEN a.poster_number END) AS poster_3,
            MAX(CASE WHEN ps_row = 4 THEN a.poster_number END) AS poster_4,
            MAX(CASE WHEN ps_row = 5 THEN a.poster_number END) AS poster_5,
            MAX(CASE WHEN ps_row = 6 THEN a.poster_number END) AS poster_6
        FROM judges j
        LEFT JOIN (
            SELECT ps.judge_id, ps.abstract_id, 
                   ROW_NUMBER() OVER (PARTITION BY ps.judge_id ORDER BY ps.abstract_id) AS ps_row
            FROM poster_score ps
        ) ps_filtered ON j.id = ps_filtered.judge_id
        LEFT JOIN abstracts a ON ps_filtered.abstract_id = a.id
        GROUP BY j.judge_number, j.first_name, j.last_name, j.department, j.hour_available
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = ["Judge Number", "First Name", "Last Name", "Department", "Hour Available",
               "Poster 1", "Poster 2", "Poster 3", "Poster 4", "Poster 5", "Poster 6"]

    df = pd.DataFrame(rows, columns=columns)
    df = df.sort_values(by="Judge Number", ascending=True)
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    excel_filename = os.path.join(output_dir,"output/judges_with_posters.xlsx")
    df.to_excel(excel_filename, index=False)
    cursor.close()
    conn.close()
    print(f"Excel file '{excel_filename}' generated successfully.")

def file3():
    conn, cursor = db.get_cursor()

    # Query to fetch all unique poster numbers
    cursor.execute("SELECT DISTINCT poster_number FROM abstracts")
    posters = [row[0] for row in cursor.fetchall()]

    # Query to fetch all unique judge numbers
    cursor.execute("SELECT DISTINCT judge_number FROM judges")
    judges = [row[0] for row in cursor.fetchall()]

    # Query to fetch all poster-judge assignments (even if no match exists)
    query = """
        SELECT a.poster_number, j.judge_number,
               CASE WHEN ps.abstract_id IS NOT NULL THEN 1 ELSE 0 END AS assigned
        FROM judges j
        CROSS JOIN abstracts a
        LEFT JOIN poster_score ps ON j.id = ps.judge_id AND a.id = ps.abstract_id
    """
    cursor.execute(query)
    assignments = cursor.fetchall()

    # Convert assignments to a Pandas DataFrame
    df = pd.DataFrame(assignments, columns=["Poster Number", "Judge Number", "Assigned"])

    # Create a complete 0-1 matrix including all posters and all judges
    matrix_df = df.pivot(index="Poster Number", columns="Judge Number", values="Assigned").fillna(0)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Save DataFrame to an Excel file
    excel_filename = os.path.join(output_dir, "poster_judge_full_matrix.xlsx")
    matrix_df.to_excel(excel_filename)

    # Close database connection
    cursor.close()
    conn.close()

    print(f"Excel file '{excel_filename}' generated successfully.")
# file1()
# file2()
# file3()