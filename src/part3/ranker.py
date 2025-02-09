import pandas as pd
from mysql.connector import Error
from src.part1.db_connection import get_db_connection
from tie_breaker import tie_resolution


def get_rank():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print('Connected to MySQL database')
            query = """
            SELECT 
                a.poster_number,
                pss.average_score,
                a.abstract AS abstract,
                j1.research_labels AS judge1_research_labels, 
                j2.research_labels AS judge2_research_labels,
                RANK() OVER (ORDER BY pss.average_score DESC) AS ranking
            FROM poster_score_summary pss
            JOIN abstracts a ON pss.abstract_id = a.id
            LEFT JOIN judges j1 ON pss.judge_id1 = j1.id
            LEFT JOIN judges j2 ON pss.judge_id2 = j2.id;
            """

            df = pd.read_sql(query, conn)
            result_dict = df.to_dict(orient='records')
            print(tie_resolution(result_dict))
            resolved_result = tie_resolution(result_dict)
            with open('final_ranking.txt', 'w') as file:
                file.write(resolved_result)

            print('Finished!!')
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print('Connection closed')


