import mysql.connector
from part1.db_connection import get_cursor

def authenticate_judge(judge_id, password):
    try:
        # Get database connection and cursor
        conn, cursor = get_cursor()
        
        # Query to check judge credentials
        query = """
        SELECT id FROM judges 
        WHERE id = %s AND password = %s;
        """
        
        cursor.execute(query, (judge_id, password))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return result is not None  # Return True if credentials are valid, else False
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

if __name__ == "__main__":
    judge_id = input("Enter Judge ID: ")
    password = input("Enter Password: ")
    
    if authenticate_judge(judge_id, password):
        print("Login successful!")
    else:
        print("Invalid credentials. Please try again.")