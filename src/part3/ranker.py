from mysql.connector import Error
from src.part1.db_connection import get_db_connection
from tie_breaker import tie_resolution
import os
import pandas as pd


def convert_text_to_csv(text: str, output_dir: str):
    lines = text.strip().split("\n")
    data_list = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        data = dict(item.split(': ') for item in line.split(', '))
        data_list.append(data)

    df = pd.DataFrame(data_list)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save as CSV
    csv_filename = os.path.join(output_dir, "final_ranking.csv")
    df.to_csv(csv_filename, index=False)

    output_dir_for_part_2 = "../part2/resources"
    os.makedirs(output_dir_for_part_2, exist_ok=True)
    csv_filename2 = os.path.join(output_dir_for_part_2, "final_ranking.csv")
    df.to_csv(csv_filename2)
    print(f"CSV file saved at: {csv_filename2}")


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
            convert_text_to_csv(resolved_result, "output")

            print('Finished!!')
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print('Connection closed')

get_rank()