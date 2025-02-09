import mysql.connector
from part1.db_connection import get_cursor

def get_assigned_posters(judge_id):
    try:
        # Get database connection and cursor
        conn, cursor = get_cursor()

        # SQL query to fetch poster IDs assigned to the given judge
        query = """
        SELECT poster_number 
        FROM judge_assignment 
        WHERE judge_id = %s;
        """
        
        cursor.execute(query, (judge_id,))
        posters = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [poster[0] for poster in posters]  # Return list of poster IDs
    except mysql.connector.Error as err:
        print("Error:", err)
        return []

if __name__ == "__main__":
    judge_id = input("Enter Judge ID: ")
    posters = get_assigned_posters(judge_id)
    print("Assigned Posters:", posters)