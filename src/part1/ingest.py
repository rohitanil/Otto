import pandas as pd
import uuid
from db_connection import get_db_connection


# Read Excel files
def read_excel(file_path):
    return pd.read_excel(file_path)


# Insert data into judges table
def insert_judges(data):
    data = data.dropna()
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
            INSERT INTO judges (id, judge_number, first_name, last_name, department, hour_available, poster_count, research_interests)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

    for _, row in data.iterrows():
        cursor.execute(query, (
            str(uuid.uuid4()),  # Generate UUID for id
            int(row["Judge"]),  # Ensure integer for judge_number
            row["Judge FirstName"],
            row["Judge LastName"],
            row["Department"],
            row["Hour available"],
            0,  # Default poster_count to 0
            None  # Insert NULL explicitly
        ))

    connection.commit()
    cursor.close()
    connection.close()


# Insert data into abstracts table
def insert_abstracts(data):
    data = data.dropna()
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO abstracts (id, poster_number, title, abstract, advisor_first_name, advisor_last_name, program)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in data.iterrows():
        cursor.execute(query, (
            str(uuid.uuid4()), row["Poster #"], row["Title"], row["Abstract"], row["Advisor FirstName"],
            row["Advisor LastName"], row["Program"]))

    connection.commit()
    cursor.close()
    connection.close()


# File paths
judges_file = "resources/Example_list_judges.xlsx"
abstracts_file = "resources/Sample_input_abstracts.xlsx"

# Read and insert data
judges_data = read_excel(judges_file)
abstracts_data = read_excel(abstracts_file)

insert_judges(judges_data)
insert_abstracts(abstracts_data)

print("Data inserted successfully!")
